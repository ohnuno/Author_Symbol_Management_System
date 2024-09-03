const createSuggestItem = element => {
    // サジェスト表示欄内で選択したアイテムの表示用データを作成する。
    const displayElement = document.getElementById(`${element.dataset.target}-display`);
    const suggestItem = document.createElement('p');
    suggestItem.dataset.pk = element.dataset.pk;
    suggestItem.dataset.target = element.dataset.target;
    suggestItem.textContent = element.textContent;
    suggestItem.classList.add('suggest-item');
    suggestItem.addEventListener('click', remove);
    displayElement.appendChild(suggestItem);
};

document.addEventListener('DOMContentLoaded', e => {
    for (const element of document.getElementsByClassName('suggest')) {
        const targetName = element.dataset.target;
        const suggestListElement = document.getElementById(`${targetName}-list`);

        // 全てのサジェスト入力欄に対しイベントを設定
        element.addEventListener('keyup', () => {
            const keyword = element.value;
            const url = `${element.dataset.url}?keyword=${keyword}`;
            if (keyword) {
                // 入力があるたびに、サーバーにそれを送信し、サジェスト候補を受け取る
                fetch(url)
                    .then(response => {
                        return response.json();
                    })
                    .then(response => {
                        const frag = document.createDocumentFragment();
                        suggestListElement.innerHTML = '';

                        // サジェスト候補を一つずつ取り出し、それを&lt;li&gt;要素として作成
                        //&lt;li&gt;要素をクリックした際のイベントも設定
                        for (const obj of response.object_list) {
                            const li = document.createElement('li');
                            li.textContent = obj.authorsymbol;
                            li.addEventListener('mousedown', clickSuggest);
                            frag.appendChild(li);
                        }

                        // サジェスト候補があればサジェスト表示欄に候補を追加し、display:block でサジェスト表示欄を見せる
                        if (frag.children.length !== 0) {
                            suggestListElement.appendChild(frag);
                            suggestListElement.style.display = 'block';

                        } else {
                            suggestListElement.style.display = 'none';
                        }

                    })
                    .catch(error => {
                        console.log(error);
                    });
            }
        });


        // 入力欄に対して、フォーカスが外れたらサジェスト表示欄を非表示にするよう設定
        element.addEventListener('blur', () => {
            suggestListElement.style.display = 'none';
        });
    }
});