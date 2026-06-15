import initSqlJs from 'sql.js';
import wasmUrl from 'sql.js/dist/sql-wasm.wasm?url';

export async function loadSongs() {
  const SQL = await initSqlJs({
    locateFile: () => wasmUrl,
  });

  const response = await fetch('/songs.sqlite');
  if (!response.ok) {
    throw new Error(`Could not load songs.sqlite: ${response.status}`);
  }

  const bytes = new Uint8Array(await response.arrayBuffer());
  const db = new SQL.Database(bytes);
  const result = db.exec(`
    select slug, title, artist, youtube_id, uploaded_at, japanese_lyrics, english_lyrics
    from songs
    order by datetime(uploaded_at) desc
  `);

  if (!result.length) {
    return [];
  }

  const { columns, values } = result[0];

  return values.map((row) => {
    const song = Object.fromEntries(columns.map((column, index) => [column, row[index]]));
    return {
      ...song,
      japaneseLyrics: JSON.parse(song.japanese_lyrics),
      englishLyrics: JSON.parse(song.english_lyrics),
    };
  });
}
