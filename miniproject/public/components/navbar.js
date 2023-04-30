function createNavbar() {
    const container = document.createElement('div');
    container.id = 'Nav_container';
    container.classList.add('navbar-container');

    const logo = document.createElement('img');
    logo.id = 'Logo';
    logo.src = './img/logo_S.png';
    logo.alt = 'Logo';

    logo.addEventListener('click', () => {
        window.location.href = 'main.html';
    });

    const searchWrapper = document.createElement('div');
    searchWrapper.classList.add('search-wrapper');

    const searchBar = document.createElement('input');
    searchBar.id = 'searchBar';
    searchBar.type = 'text';
    searchBar.placeholder = '검색';

    searchBar.addEventListener('keyup', function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            search();
        }
    });

    const searchButton = document.createElement('button');
    searchButton.id = 'searchButton';
    searchButton.textContent = '검색';

    searchButton.addEventListener('click', () => {
        search();
    });

    function search() {
        const searchQuery = searchBar.value.trim();
        if (searchQuery) {
            window.location.href = `search.html?q=${searchQuery}`;
        }
    }

    searchWrapper.appendChild(searchBar);
    searchWrapper.appendChild(searchButton);

    const loginButton = document.createElement('button');
    loginButton.id = 'loginButton';
    loginButton.textContent = 'Log in';

    container.appendChild(logo);
    container.appendChild(searchWrapper);
    container.appendChild(loginButton);

    return container;
}

document.addEventListener('DOMContentLoaded', function () {
    const navbar = createNavbar();
    document.body.appendChild(navbar);
});
