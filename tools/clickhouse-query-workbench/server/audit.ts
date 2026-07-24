import { mkdir, readFile, writeFile, appendFile } from "node:fs/promises";
import path from "node:path";
import { nanoid } from "nanoid";
import { config } from "./config";

export type AuditRecord = {
  id: string;
  type: "query" | "favorite";
  createdAt: string;
  sql: string;
  note?: string;
  ok?: boolean;
  elapsedMs?: number;
  rowCount?: number;
  error?: string;
};

const historyFile = () => path.join(process.cwd(), config.auditDir, "query-history.jsonl");
const favoritesFile = () => path.join(process.cwd(), config.auditDir, "favorites.json");

export const appendHistory = async (record: Omit<AuditRecord, "id" | "createdAt" | "type">): Promise<AuditRecord> => {
  await mkdir(path.dirname(historyFile()), { recursive: true });
  const fullRecord: AuditRecord = {
    id: nanoid(),
    type: "query",
    createdAt: new Date().toISOString(),
    ...record
  };
  await appendFile(historyFile(), `${JSON.stringify(fullRecord)}\n`, "utf8");
  return fullRecord;
};

export const readHistory = async (): Promise<AuditRecord[]> => {
  try {
    const content = await readFile(historyFile(), "utf8");
    return content
      .split(/\r?\n/)
      .filter(Boolean)
      .map((line) => JSON.parse(line) as AuditRecord)
      .reverse()
      .slice(0, 200);
  } catch {
    return [];
  }
};

export const readFavorites = async (): Promise<AuditRecord[]> => {
  try {
    return JSON.parse(await readFile(favoritesFile(), "utf8")) as AuditRecord[];
  } catch {
    return [];
  }
};

export const saveFavorite = async (sql: string, note?: string): Promise<AuditRecord> => {
  await mkdir(path.dirname(favoritesFile()), { recursive: true });
  const favorites = await readFavorites();
  const record: AuditRecord = {
    id: nanoid(),
    type: "favorite",
    createdAt: new Date().toISOString(),
    sql,
    note
  };
  favorites.unshift(record);
  await writeFile(favoritesFile(), JSON.stringify(favorites.slice(0, 200), null, 2), "utf8");
  return record;
};

export const deleteFavorite = async (id: string): Promise<void> => {
  const favorites = await readFavorites();
  await mkdir(path.dirname(favoritesFile()), { recursive: true });
  await writeFile(favoritesFile(), JSON.stringify(favorites.filter((item) => item.id !== id), null, 2), "utf8");
};

