
$(document).ready(function () {
  if (typeof jquery === 'undefined') {
    // jQuery IS NOT loaded, do stuff here.
    alert('Jquery not installed')
  }
  // do stuff when DOM is ready

  const btn = document.getElementById('button')

  function sendReference (reference) {
    const XHR = new XMLHttpRequest()
    const url = ''

    const data = $('form').serializeArray()
    console.log(data)

    // var data = JSON.stringify({})
    XHR.open('POST', 'http:localhost:5000/reference-db')
    xhr.send(data)
  }

  btn.addEventListener('click', function () {
    sendReference()
  })
})
