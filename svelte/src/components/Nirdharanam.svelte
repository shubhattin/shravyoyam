<script lang="ts">
  import IoClose from 'svelte-icons-pack/io/IoClose';
  import Icon from 'svelte-icons-pack/Icon.svelte';
  import { dattAMsh, LOC_ID, nirdharanam } from '@store/index';
  import loadData from '@tools/LoadData';

  let loc = '';
  let displayLoc = localStorage.getItem(LOC_ID);
  let data_view = false;
  let inputRef: HTMLInputElement = null!;

  const store = async () => {
    if (loc === '') return;
    let v = await loadData(loc);
    if (JSON.stringify(v) !== '{}') {
      localStorage.setItem(LOC_ID, loc);
      displayLoc = loc;
      dattAMsh.set(v);
      data_view = true;
      loc = '';
    } else {
      const style = inputRef.style;
      style.color = 'red';
      style.backgroundColor = 'white';
      setTimeout(() => {
        style.color = '';
        style.backgroundColor = '';
      }, 600);
    }
  };
</script>

<div class="fixed bottom-7 left-5">
  <div>
    <input
      type="text"
      autocapitalize="off"
      bind:this={inputRef}
      bind:value={loc}
      class="w-52 p-1 ml-0 text-white bg-black font-medium m-1 border-2 border-white rounded-lg"
    />
    <button
      on:dblclick={store}
      class="text-white p-1 border-2 border-yellow-400 m-1 rounded-md active:text-blue-400 active:border-green-500"
    >
      ok
    </button>
    <button
      on:click={() => (data_view = true)}
      class="text-white p-1 border-2 border-yellow-400 m-1 rounded-md active:text-red-400 active:border-green-500"
    >
      s
    </button>
    <button on:click={() => nirdharanam.set(false)}>
      <Icon src={IoClose} className="w-11 h-11 cursor-pointer -ml-2 inline-block fill-red-500" />
    </button>
  </div>
  {#if data_view}
    <div class="text-white text-sm overflow-scroll max-w-xs max-h-32">
      <div>{displayLoc}</div>
      <br />
      <div>{JSON.stringify($dattAMsh)}</div>
    </div>
  {/if}
</div>
