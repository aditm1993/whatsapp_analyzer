const checkbox = (checkboxId) => {
    document.querySelector(`#${checkboxId}`).click();
}

const checkAll = () => {
    for (const row of document.querySelectorAll('.checkbox'))
        row.checked = true;
}

const uncheckAll = () => {
    for (const row of document.querySelectorAll('.checkbox'))
        row.checked = false;
}
const downloadCsv = () => {

}

