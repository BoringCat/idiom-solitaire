

$(window).ready(() => {
    $('#m .button').click(() => {
        $('#c').removeAttr('disabled')
    })
    $('#c').click(connectsocket)
    $('#s').click(submit)
    $('#i').keydown(e=>{
        if ( e.which == 13 ) submit()
    })
})
const submit = () => {
    $('#s').attr('disabled', '');
    addToList('', '你: ' + $('#i').val())
    socket.send($('#i').val())
    $('#i').val('')
}
var socket,
    ismodeselect = isconnect = false,
    i = 0
const addToList = (style, text) => {
    i++;
    $('#l').append('<li class="listitem ' + style + '">' + text + '</li>')
    $('#l').scrollTop(i * 40)
}
const connectsocket = () => {
    let host = window.location.host,
        protocol = window.location.protocol == 'https:' ? 'wss:' : 'ws:'
    socket = new WebSocket(protocol + '//' + host + '/cyjl')
    $('#ic').addClass('hidden')
    $('#dc').addClass('hidden')
    $('#ci').removeClass('hidden')
    $('#l').empty()
    i = 0
    socket.onmessage = e => {
        try {
            var dict = JSON.parse(e.data)
        } catch (error) {
            addToList('bg-reg', '发生未知错误')
            console.error(error)
            socket.close()
            return
        }
        switch (dict.action) {
            case "init":
                init = {
                    'action': "connect",
                    'mode': $('label.active input[type="radio"]').val(),
                    'length': $('#le').val(),
                    'noyd': ($('.button.active input[name="noyd"]').val() || 'False')
                }
                socket.send(JSON.stringify(init))
                $('#c').attr('disabled', '')
                break
            case "disconnect":
                addToList('bg-reg', dict.msg)
                break
            case "connect":
                if (dict.youfirst) {
                    addToList('bg-green', '你先 :)')
                } else {
                    addToList('bg-red', '电脑先 :(')
                    addToList('', '电脑: ' + dict.output)
                    if (dict.extra) addToList('bg-mix', '电脑: ' + dict.extra)
                }
                $('#s').removeAttr('disabled')
                $('#i').removeAttr('disabled')
                $('#c').removeClass('bg-mix')
                $('#c').removeClass('bg-red')
                $('#c').addClass('bg-green')
                $('#ic').removeClass('hidden')
                $('#dc').addClass('hidden')
                $('#ci').addClass('hidden')
                break
            case "msg":
                addToList('', '电脑: ' + dict.output)
                if (dict.extra) addToList('bg-mix', '电脑: ' + dict.extra)
                $('#s').removeAttr('disabled')
                break
            case "finish":
                if (dict.status) {
                    addToList('bg-green', '电脑GG了');
                    addToList('bg-green', '你赢了')
                } else {
                    addToList('bg-red', '你GG了');
                    if (dict.output) addToList('bg-mix', dict.output)
                }
                break
            default:
                addToList('bg-reg', '发生未知错误')
                console.error(dict)
                socket.close()
                break
        }
    }
    socket.onclose = socket.onerror = e => {
        $('#dc').removeClass('hidden');
        $('#ic').addClass('hidden');
        $('#ci').addClass('hidden');
        $('#c').removeClass('bg-mix');
        $('#c').removeClass('bg-green');
        $('#c').addClass('bg-red');
        ismodeselect = false;
        $('#s').attr('disabled', '');
        $('#i').attr('disabled', '');
        $('#c').removeAttr('disabled')
    }
}
