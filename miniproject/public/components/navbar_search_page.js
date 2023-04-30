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


    const loginButton = document.createElement('button');
    loginButton.id = 'loginButton';
    loginButton.textContent = 'Log in';

    container.appendChild(logo);
    container.appendChild(loginButton);

    return container;
}

document.addEventListener('DOMContentLoaded', function () {
    const navbar = createNavbar();
    document.body.appendChild(navbar);
});
