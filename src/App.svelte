<script>
  import { flushSync, onMount, tick } from 'svelte';
  import { loadSongs } from './songs.js';

  let route = routeFromHash();
  let songs = [];
  let loadingSongs = true;
  let songError = '';

  $: currentSong = route.name === 'song'
    ? songs.find((song) => song.slug === route.slug)
    : null;

  function routeFromHash() {
    const hash = window.location.hash.replace(/^#/, '');
    const match = hash.match(/^\/songs\/([^/]+)$/);
    return match ? { name: 'song', slug: decodeURIComponent(match[1]) } : { name: 'home' };
  }

  async function transitionTo(update) {
    if ('startViewTransition' in document) {
      const transition = document.startViewTransition(() => {
        flushSync(update);
      });

      transition.ready.catch(() => {});
      transition.updateCallbackDone.catch(() => {});
      await transition.finished.catch(() => {});
      return;
    }

    update();
    await tick();
  }

  function openSong(song) {
    transitionTo(() => {
      route = { name: 'song', slug: song.slug };
      history.pushState({}, '', `#/songs/${encodeURIComponent(song.slug)}`);
    });
  }

  function openHome() {
    transitionTo(() => {
      route = { name: 'home' };
      history.pushState({}, '', '#/');
    });
  }

  onMount(async () => {
    const handlePop = () => {
      transitionTo(() => {
        route = routeFromHash();
      });
    };

    window.addEventListener('popstate', handlePop);

    try {
      songs = await loadSongs();
    } catch (error) {
      songError = error.message;
    } finally {
      loadingSongs = false;
    }

    return () => window.removeEventListener('popstate', handlePop);
  });
</script>

<svelte:head>
  <meta
    name="description"
    content="A dark 1999-style personal site with Japanese song lyrics, translations, projects, and interests."
  />
</svelte:head>

<div class="scanlines" aria-hidden="true"></div>
<div class="dvd-field" aria-hidden="true">
  <div class="dvd-track-y">
    <img class="dvd-gif" src="/assets/keikaku.gif" alt="" />
  </div>
</div>

{#if route.name === 'home'}
  <main class="site-shell home-view">
    <header class="masthead">
      <div class="status-strip">
        <span>LAST UPDATED: 2026-06-15</span>
        <span>BEST VIEWED IN 800x600</span>
      </div>
      <h1>LUKE BURROUGH</h1>
    </header>

    <section class="home-grid">
      <article class="pixel-box about-box">
        <h2>about me</h2>
        <nav class="button-stack" aria-label="About me links">
          <a href="/resume.pdf">resume</a>
          <a href="/projects">projects</a>
          <a href="/experience">experience</a>
        </nav>
      </article>

      <article class="pixel-box songs-box">
        <div class="box-heading-row">
          <h2>song lyrics and translations</h2>
        </div>

        {#if loadingSongs}
          <p class="terminal-line">loading songs.sqlite...</p>
        {:else if songError}
          <p class="terminal-line error">{songError}</p>
        {:else}
          <ol class="song-list">
            {#each songs as song}
              <li>
                <button type="button" class="song-link" on:click={() => openSong(song)}>
                  <span class="song-title" style={`view-transition-name: song-title-${song.slug}`}>
                    {song.title}
                  </span>
                  <span class="song-meta">{song.artist} // {song.uploaded_at}</span>
                </button>
              </li>
            {/each}
          </ol>
        {/if}
      </article>

      <article class="pixel-box interests-box">
        <h2>interests</h2>
        <ul class="interest-list">
          <li>japanese language</li>
          <li>music</li>
          <li>pure math</li>
        </ul>
      </article>
    </section>

    <footer class="footer-bar">
      <a href="mailto:lukeburrough26@gmail.com">lukeburrough26@gmail.com</a>
    </footer>
  </main>
{:else}
  <main class="song-page">
    {#if currentSong}
      <button class="back-link" type="button" on:click={openHome}>back</button>

      <header class="song-header">
        <h1 style={`view-transition-name: song-title-${currentSong.slug}`}>{currentSong.title}</h1>
        <p>{currentSong.artist}</p>
      </header>

      <aside class="video-dock" aria-label="YouTube video">
        <iframe
          src={`https://www.youtube.com/embed/${currentSong.youtube_id}`}
          title={`${currentSong.title} by ${currentSong.artist}`}
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          allowfullscreen
        ></iframe>
      </aside>

      <section class="lyrics-board" aria-label="Lyrics and translation">
        {#each currentSong.japaneseLyrics as stanza, stanzaIndex}
          <div class="stanza">
            {#each stanza as line, lineIndex}
              <p class="lyric-row">
                <span lang="ja">{line}</span>
                <span>{currentSong.englishLyrics[stanzaIndex][lineIndex]}</span>
              </p>
            {/each}
          </div>
        {/each}
      </section>
    {:else}
      <button class="back-link" type="button" on:click={openHome}>back</button>
      <section class="pixel-box missing-song">
        <h1>song not found</h1>
        <p>The SQLite index loaded, but this slug is not in it.</p>
      </section>
    {/if}
  </main>
{/if}
