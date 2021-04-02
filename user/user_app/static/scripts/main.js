const options = {
  rootMargin: '-40% 0% -60% 0%',
  // current ff-esr needs -39.5% margin to respond.
  // reported solved in ff-release: https://bugzilla.mozilla.org/show_bug.cgi?id=1553673
  threshold: 0.0
}

let routePath = '/'
let titleView = true
let currentSlug = null

const setRoute = (route) => {
  routePath = route
}

const observerCallback = (entries) => {
  entries.forEach(entry => {
    const targetId = entry.target.getAttribute('id')

    if (entry.isIntersecting === true) {
      currentSlug = targetId
      if (titleView === true) {
        document.getElementById(`sidebar_${targetId}`).classList.add('selected-title')
      } else {
        pullMetadata()
      }
    } else if (titleView === true) {
      // MDN: If the string is not in the list, no error is thrown, and nothing happens.
      document.getElementById(`sidebar_${targetId}`).classList.remove('selected-title')
    }
  }
  )
}
const observer = new IntersectionObserver(observerCallback, options)

window.onload = () => { // waits for the page to load. Investigate async/defer.
  document.querySelector('#sidebar-tab-hotload').style.display = 'block'

  const targets = document.querySelectorAll('.article')
  targets.forEach(target => {
    observer.observe(target)
  })
}

const displayTitles = (titles = 'Jinja provided no titles') => {
  document.querySelector('#sidebar-content').innerHTML = titles
  document.querySelector(`#sidebar_${currentSlug}`).classList.add('selected-title')
  titleView = true
}

const pullMetadata = (slug = currentSlug) => {
// what is preventDefault about?
  window.fetch(routePath,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(slug)
    })
    .then(parseJSON)
    .then(displaySemantics)
}

const parseJSON = (response) => response.json()

const displaySemantics = (data) => {
  let tagLinks = ''
  for (const i in data.tags_list) {
    tagLinks = tagLinks +
     `<a href="/tag/${data.tags_list[i].name}">${data.tags_list[i].name}</a><br>`
  }
  const html =
   `
   Tags:<br>
      ${tagLinks} <br>
    Epistemic_state: ${data.epistemic_state.name} <br><br>
    Last major edit: ${JSON.stringify(data.last_major_edit)} <br>
   `
  document.querySelector('#sidebar-content').innerHTML = html
  titleView = false // placed last to be skipped in case above operations fail
}
