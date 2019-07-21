copy(
    Array.from(document.getElementsByClassName('linkSenatore'))
        .map(unSenatore => unSenatore.getElementsBySelector('a')
            .map(a => a.text.replace(',', ';'))
            .join(',')
        )
        .join('\n')
)

copy(
    (Array.from(
        document
            .getElementsByClassName('tabellaXHTML')[0]
            .querySelector('tbody')
            .querySelectorAll('tr'))
                .map(row => row.innerText)
                .map(text => text.replace('\t', ','))
    ).join('\n')
)
