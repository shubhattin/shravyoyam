<script lang="ts">
  import { lasanSanchit, LOC_ID, lasan, currentTime } from '@store/index';
</script>

{#if $lasan && $lasanSanchit[1][0] !== ''}
  {@const dt = $lasanSanchit[1]}
  {@const src = `${localStorage.getItem(LOC_ID)}/${dt[0]}`}
  {#if dt[2] === 0}
    <audio bind:currentTime={$currentTime} controls loop autoPlay {src} />
  {:else if dt[2] === 1}
    <!-- svelte-ignore a11y-media-has-caption -->
    <video class="w-full h-full" bind:currentTime={$currentTime} controls loop autoPlay {src} />
  {/if}
{/if}
