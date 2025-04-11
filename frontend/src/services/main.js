export function dateToString() {
  const date = new Date();
  let year = date.getFullYear();
  let month = String(date.getMonth() + 1).padStart(2, "0");
  let day = String(date.getDate()).padStart(2, "0");
  let hour = String(date.getHours()).padStart(2, "0");
  let minute = String(date.getMinutes()).padStart(2, "0");
  let second = String(date.getSeconds()).padStart(2, "0");
  let millisecond = String(date.getMilliseconds()).padStart(2, "0");
  return `${year}${month}${day}${hour}${minute}${second}${millisecond}`;
}
export function sortByDate(dataLst, order = "asc") {
  const sorted = [...dataLst];
  return order === "desc"
    ? sorted.sort(
        (a, b) => new Date(b.formattedDate) - new Date(a.formattedDate)
      )
    : sorted.sort(
        (a, b) => new Date(a.formattedDate) - new Date(b.formattedDate)
      );
}
