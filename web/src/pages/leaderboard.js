import { getLeaderBoardData } from "../utils/fetchUtils.js";


export async function Leaderboard(req) {
    const root = document.querySelector("#root");
    root.innerHTML = `
    <div class="container table-container">
        <h1>Tulostaulut</h1>
        <p>Valitse suodatin ja järjestys</p>
        <form id="leaderboard-filter">
            <select name="filter">
                <option value="total_winnings" selected>Kokonaisvoitot</option>
                <option value="games_played">Pelatut pelit</option>
                <option value="games_won">Voitetut pelit</option>
                <option value="games_lost">Hävityt pelit</option>
            </select>
            <select name="sort">
                <option value="asc">Nouseva</option>
                <option value="desc" selected>Laskeva</option>
            </select>
            <input type="submit" value="Suodata"/>
        </form>
        <table id="leaderboard">  
        </table>
    </div>
    `;

    initializeLeaderboard()
}

// matches the names from db query
const tableColumns = [
    'käyttäjänimi',
    'kokonaisvoitot',
    'pelejä pelattu',
    'pelejä voitettu',
    'pelejä hävitty',
]

function createTable(data, destination) {
    destination.innerHTML = '';

    const thead = document.createElement('thead');
    const headTr = document.createElement('tr');
    const tbody = document.createElement('tbody');

    // create the header row
    tableColumns.forEach(column => {
        const th = document.createElement('th');
        th.textContent = column;
        headTr.appendChild(th);
    });

    thead.appendChild(headTr);

    // create the data rows
    data.forEach(row => {
        const tr = document.createElement('tr');
        const sortedRow = sortObjectByOrder(row, tableColumns)

        Object.values(sortedRow).forEach(column => {
            const td = document.createElement('td');
            td.textContent = column;
            tr.appendChild(td);
        });

        tbody.appendChild(tr);
    });

    destination.appendChild(thead);
    destination.appendChild(tbody);
}

// sort the object by the order of the keys in the order array
function sortObjectByOrder(obj, order) {
    return order.reduce((sorted, key) => {
        if (obj.hasOwnProperty(key)) {
            sorted[key] = obj[key];
        }
        return sorted;
    }, {});
}

async function initializeLeaderboard() {
    const table = document.querySelector('table#leaderboard')
    const filterForm = document.querySelector('form#leaderboard-filter')

    // listen to changes in the filtering
    filterForm.addEventListener('submit', async (e) => {
        e.preventDefault()

        // get the form values
        const filter = filterForm.querySelector('[name="filter"]').value
        const sort = filterForm.querySelector('[name="sort"]').value

        const filteredData = await getLeaderBoardData({
            filter: filter,
            sort: sort,
        })

        createTable(filteredData, table)
    });

    const initialData = await getLeaderBoardData({
        filter: 'total_winnings',
        sort: 'desc'
    })
    createTable(initialData, table)
}