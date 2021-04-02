window.onload = () => { // waits for the page to load. Investigate async/defer.
  document.querySelector('.logo').innerHTML = backButton
}

const backButton =
`
<a style="display: block; margin: inherit; width: 2em" onclick="history.back()" href="#">
    <img src="/static/assets/back-arrow.svg">
</a>
`
