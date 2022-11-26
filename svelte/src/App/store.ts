import { writable } from 'svelte/store';
import type { datt_type } from './tools/LoadData';

export const blinking = writable(false);
export const nirdharanam = writable(false);
export const lasan = writable(false);
export const lasanSanchit = writable<[string, [string, string, number]]>(['', ['', '', 0]]);
export const media_show = writable(false);
export const dattAMsh = writable<datt_type>({});
export const LOC_ID = 'sthAnam';
