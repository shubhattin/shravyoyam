export interface datt_type {
  [x: string]: [string, string, number];
}
const loadData = (lc: string) =>
  new Promise<datt_type>((rs) => {
    let e = document.createElement('script');
    e.src = lc + '/saYc.js';
    document.body.appendChild(e);
    e.onload = () => {
      e.remove();
      // @ts-ignore
      rs(data !== undefined ? data : {});
    };
    e.onerror = () => {
      e.remove();
      rs({});
    };
  });
export default loadData;
