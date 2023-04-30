function createFooter() {
    const container = document.createElement('footer');
    container.id = 'footer';

    const logo = document.createElement('img');
    logo.id = 'footer_Logo';
    logo.src = './img/logo.png';
    logo.alt = 'Logo';

    const linkContainer = document.createElement('div');
    linkContainer.id = 'link-container';

    const helpLink = document.createElement('a');
    helpLink.href = 'https://github.com/impelfin';
    helpLink.textContent = '도움주신분';

    const divider = document.createElement('span');
    divider.textContent = ' | ';

    const copyRight = document.createElement('p');
    copyRight.textContent = 'ⓒ 2023 NineBrary, Inc. All Rights Reserved.';

    linkContainer.appendChild(helpLink);
    linkContainer.appendChild(divider);
    linkContainer.appendChild(copyRight);

    container.appendChild(logo);
    container.appendChild(linkContainer);

    return container;
}

document.addEventListener('DOMContentLoaded', function () {
    const footer = createFooter();
    document.body.appendChild(footer);
});
