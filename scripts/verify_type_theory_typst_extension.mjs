#!/usr/bin/env node
/* Production SNL Doc Extension gate for opaque Macro-level Typst metadata. */
import fs from "node:fs/promises";
import path from "node:path";
import assert from "node:assert/strict";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const workspace = path.resolve(process.argv[2] || path.join(__dirname, ".."));
const extensionRepo = path.resolve(process.argv[3] || process.env.SNL_EXTENSION_REPO || "");
if (!extensionRepo || extensionRepo === path.parse(extensionRepo).root) {
  throw new Error("usage: verify_type_theory_typst_extension.mjs [workspace] <SNL-Doc-Extension-repo>");
}
const io = require(path.join(extensionRepo, "out", "entityStorageIo.js"));
const migrations = require(path.join(extensionRepo, "out", "dataMigrations.js"));
const doc = path.join(workspace, ".SNL_Doc");
const extensionKey = "x_fulcrum_typst";

async function jsonFile(file) {
  return JSON.parse(await fs.readFile(file, "utf8"));
}
async function directoryMap(directory) {
  const result = new Map();
  for (const file of (await fs.readdir(path.join(doc, directory))).filter((name) => name.endsWith(".json")).sort()) {
    result.set(`${directory}/${file}`, await jsonFile(path.join(doc, directory, file)));
  }
  return result;
}
function storageFromMap(values) {
  return {
    async listJsonFiles(directory) {
      return [...values.keys()].filter((key) => key.startsWith(`${directory}/`)).map((key) => key.slice(directory.length + 1));
    },
    async readJson(relative) {
      return values.has(relative) ? structuredClone(values.get(relative)) : null;
    },
  };
}
function extensions(records) {
  return records.filter((record) => Object.hasOwn(record.macro, extensionKey));
}
function assertRoundTrips(records, label) {
  const selected = extensions(records);
  assert.equal(selected.length, 63, `${label}: exact extension count`);
  const bindings = new Set();
  for (const record of selected) {
    const exact = structuredClone(record.macro[extensionKey]);
    const rewrite = io.rewriteMacroEntityRecord(record, record.envelope.package, structuredClone(record.macro));
    assert.deepEqual(rewrite.value.macro[extensionKey], exact, `${label}: exact x field survives rewrite`);
    assert.ok(!bindings.has(exact.binding), `${label}: duplicate binding ${exact.binding}`);
    bindings.add(exact.binding);
  }
}

const macroEntities = await directoryMap("macros");
const rawRecords = await io.readMacroEntityRecords(storageFromMap(macroEntities), "11");
assertRoundTrips(rawRecords, "production predecessor-reader");

// Exercise the real 0.0.11 -> 0.1.0 migration. This edge changes only the
// workspace version marker; Macro payloads, including opaque fields, must be byte-equivalent JSON values.
const config = await jsonFile(path.join(doc, "config.json"));
config.version = "0.0.11";
const snapshot = {
  config,
  macroPackages: new Map(),
  relationships: await jsonFile(path.join(doc, "relationships.json")),
  entries: await jsonFile(path.join(doc, "entries.json")),
  packageManifests: await directoryMap("packages"),
  entryEntities: await directoryMap("entries"),
  macroEntities: new Map([...macroEntities].map(([key, value]) => [key, structuredClone(value)])),
};
const macroBefore = JSON.stringify([...snapshot.macroEntities]);
const report = await migrations.migrateWorkspaceSnapshot(snapshot, () => {
  throw new Error("0.0.11 marker-only migration must not canonicalize Macro packages");
});
assert.deepEqual(report.applied.map((edge) => `${edge.from}->${edge.to}`), ["0.0.11->0.1.0"]);
assert.equal(snapshot.config.version, "0.1.0");
assert.equal(JSON.stringify([...snapshot.macroEntities]), macroBefore, "marker-only migration changed Macro entities");
const migratedRecords = await io.readMacroEntityRecords(storageFromMap(snapshot.macroEntities), "11");
assertRoundTrips(migratedRecords, "production post-migration-reader");

// The host still rejects its reserved Macro-level `typst` key while accepting x_fulcrum_typst.
const poisoned = new Map([...macroEntities].map(([key, value]) => [key, structuredClone(value)]));
const firstKey = [...poisoned.keys()][0];
poisoned.get(firstKey).macro.typst = {};
await assert.rejects(() => io.readMacroEntityRecords(storageFromMap(poisoned), "11"), /typst.*Macro|Macro.*typst/i);

console.log(JSON.stringify({
  extension_commit: require(path.join(extensionRepo, "package.json")).version,
  macro_records: rawRecords.length,
  declarations: extensions(rawRecords).length,
  migration: "0.0.11->0.1.0",
  roundtrips: 126,
  reserved_typst_rejected: true,
}));
