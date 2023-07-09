<script lang="ts">
  import { clsx } from '@tools/clsx';
  import { onMount } from 'svelte';
  import loadData from '@tools/LoadData';
  import {
    LOC_ID,
    lasan,
    nirdharanam,
    lasanSanchit,
    dattAMsh,
    media_show,
    blinking,
    fileName,
    currentTime
  } from '@store/index';
  import Blink from '@components/Blink.svelte';
  import Player from '@components/Player.svelte';

  let prachalan = false;
  let chalan = false;
  let value = '';

  let collect: number[] = [];
  let key_num = 0;
  let body: HTMLDivElement = null!;
  const todani = (n: number) => {
    collect.push(n);
    if (prachalan && n === 1 && collect.length == 1) set_media_file(value);
    let jn = collect.join('');
    if (chalan) {
      if (jn === '12') prachalan = true;
      else if (jn == '21') {
        chalan = false; //active state of app
        prachalan = false; //active state of input field
        $lasan = false; // state of current playback
      }
      if (jn.length === 2) {
        collect = [];
        $blinking = true;
      }
    } else {
      if (jn === '22112') {
        body.style.backgroundColor = 'purple';
        setTimeout(() => {
          body.style.backgroundColor = '';
          chalan = true;
        }, 500);
      } else if (jn == '22212') {
        $nirdharanam = true; // nirdharanam page
      }
      if (collect.length === 5) {
        collect = [];
        $blinking = true;
      }
    }
  };
  const check = () => {
    if (prachalan) {
      key_num++;
      setTimeout(() => {
        if (key_num == 0) return;
        else if (key_num == 1) {
          set_media_file(value); // this will set if any available else set it zero
        }
        key_num--;
      }, 3000);
    } else value = '';
  };
  const set_media_file = (val: string) => {
    if (val != '' && val in $dattAMsh) {
      $lasan = true;
      $fileName = val;
      $lasanSanchit = [val, $dattAMsh[val]];
      prachalan = false;
      $media_show = false;
    }
    value = '';
    if (val !== '') collect = [];
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

<svelte:head>
  <title>లస్యశ్రవ్యౌ</title>
</svelte:head>
<div
  bind:this={body}
  class={clsx(
    'p-2 w-screen h-screen select-none transition',
    JSON.stringify($dattAMsh) !== '{}' ? 'bg-black' : 'bg-neutral-900'
  )}
>
  <div class={prachalan ? undefined : 'hidden'}>
    <form on:submit|preventDefault={() => set_media_file(value)}>
      <input
        on:input={check}
        autocapitalize="off"
        bind:value
        type="text"
        class="w-52 ml-0 text-teal-500 bg-black block font-semibold m-1 text-xl border-2 border-gray-900 rounded-md"
      />
    </form>
    <select
      bind:value={$fileName}
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
      {#await import('@components/TimeControl.svelte') then TimeControl}
        <TimeControl.default />
      {/await}
      <Player />
    </div>
  {/if}
  <Blink />
  {#if $nirdharanam}
    {#await import('@components/Nirdharanam.svelte') then Nirdharanam}
      <Nirdharanam.default />
    {/await}
  {/if}
</div>
