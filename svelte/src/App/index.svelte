<script lang="ts">
  import { clsx } from './tools/clsx';
  import { writable } from 'svelte/store';
  import { onMount } from 'svelte';
  import loadData from './tools/LoadData';
  // import TimeControl from './components/TimeControl.svelte';
  import {
    LOC_ID,
    lasan,
    nirdharanam,
    lasanSanchit,
    dattAMsh,
    media_show,
    blinking
  } from './store';
  import Blink from './components/Blink.svelte';
  import Nirdharanam from './components/Nirdharanam.svelte';

  const prachalan = writable(false);
  const chalan = writable(false);
  const value = writable('');
  const selectValue = writable('');

  let collect: number[] = [];
  let key_num = 0;
  let body: HTMLDivElement = null!;
  let media_ref: HTMLAudioElement | HTMLVideoElement = null!;

  const todani = (n: number) => {
    collect.push(n);
    if ($prachalan && n === 1 && collect.length == 1) set_media_file($value);
    let jn = collect.join('');
    if ($chalan) {
      if (jn === '12') prachalan.set(true);
      else if (jn == '21') {
        chalan.set(false); //active state of app
        prachalan.set(false); //active state of input field
        lasan.set(false); // state of current playback
      }
      if (jn.length === 2) {
        collect = [];
        blinking.set(true);
      }
    } else {
      if (jn === '22112') {
        body.style.backgroundColor = 'purple';
        setTimeout(() => {
          body.style.backgroundColor = '';
          chalan.set(true);
        }, 500);
      } else if (jn == '22212') nirdharanam.set(true);
      if (collect.length === 5) {
        collect = [];
        blinking.set(true);
      }
    }
  };
  const check = () => {
    if (prachalan) {
      key_num++;
      setTimeout(() => {
        if (key_num == 0) return;
        else if (key_num == 1) value.set('');
        key_num--;
      }, 3000);
    } else value.set('');
  };
  const set_media_file = (vl: string) => {
    if (vl != '' && vl in $dattAMsh) {
      lasan.set(true);
      lasanSanchit.set([vl, $dattAMsh[vl]]);
      prachalan.set(false);
      media_show.set(false);
    }
    value.set('');
    if (vl !== '') collect = [];
  };

  onMount(() => {
    if (LOC_ID in localStorage) {
      loadData(localStorage.getItem(LOC_ID) || '').then((v) => {
        if (JSON.stringify(v) !== '{}') dattAMsh.set(v);
      });
    }
  });
  $: !$lasan && lasanSanchit.set(['', ['', '', 0]]); // removing current playing if lasan goes off
</script>

<div
  bind:this={body}
  class={clsx(
    'p-2 w-full h-full select-none fixed top-0',
    JSON.stringify($dattAMsh) !== '{}' ? 'bg-black' : 'bg-stone-900'
  )}
>
  <div class={$prachalan ? '' : 'hidden'}>
    <form
      on:submit={(e) => {
        e.preventDefault();
        set_media_file($value);
      }}
    >
      <input
        on:input={check}
        bind:value={$value}
        type="text"
        class="w-52 ml-0 text-teal-500 bg-black block font-semibold m-1 text-xl border-2 border-gray-900 rounded-md"
      />
    </form>
    <select
      bind:value={$selectValue}
      on:change={(e) => set_media_file(e.currentTarget.value)}
      class="w-5 h-4 mt-2 text-white bg-black outline-none border-2 rounded-sm border-gray-900"
    >
      {#each Object.keys($dattAMsh) as val}
        <option value={val}>
          {$dattAMsh[val][1]} :- {val}
          {['🎵', '📀'][$dattAMsh[val][2]]}
        </option>
      {/each}
    </select>
  </div>
  <div class="fixed z-50 top-2.5 left-[225px]">
    <button
      on:click={() => todani(1)}
      on:dblclick={() => lasan && media_show.update((v) => !v)}
      class="sam bg-[#ff0] border-transparent border-2 font-bold py-1.5 px-2 rounded-md focus:border-red-500 focus:outline-none active:border-blue-600 active:bg-amber-200"
    >
      ௰
    </button>
    <button
      on:click={() => todani(2)}
      on:dblclick={() => chalan && lasan.set(false)}
      class="sam bg-[greenyellow] ml-4 border-transparent border-2 font-bold py-1.5 px-2 rounded-md focus:border-red-500 focus:outline-none active:border-blue-600 active:bg-lime-300"
    >
      ௲
    </button>
  </div>
  {#if $lasan}
    <div class={$media_show ? '' : 'hidden'}>
      {#await import('./components/TimeControl.svelte') then TimeControl}
        <TimeControl.default elm={media_ref} />
      {/await}
      {#if $lasan && $lasanSanchit[1][0] !== ''}
        {@const dt = $lasanSanchit[1]}
        {@const lc = `${localStorage.getItem(LOC_ID)}/${dt[0]}`}
        {#if dt[2] === 0}
          <audio bind:this={media_ref} controls loop autoPlay src={lc} />
        {:else if dt[2] === 1}
          <!-- svelte-ignore a11y-media-has-caption -->
          <video bind:this={media_ref} controls loop autoPlay src={lc} />;
        {/if}
      {/if}
    </div>
  {/if}
  <Blink />
  {#if $nirdharanam}
    {#await import('./components/Nirdharanam.svelte') then Nirdharanam}
      <Nirdharanam.default />
    {/await}
  {/if}
</div>
