

$(window).ready(() => {
    $('#mode .button').click(() => {
        $('#connect').removeAttr('disabled')
    })
    $('#submit').click(() => {
        $('#submit').attr('disabled', '');
        addToList('', '你: ' + $('#idiom').val())
        socket.send($('#idiom').val())
        $('#idiom').val('')
    })
})
var socket,
    ismodeselect = isconnect = false,
    i = 0
const addToList = (style, text) => {
    i++;
    $('#list').append('<li class="listitem ' + style + '">' + text + '</li>')
    $('#list').scrollTop(i * 40)
}
const connectsocket = () => {
    let host = window.location.host,
        protocol = window.location.protocol == 'https:' ? 'wss:' : 'ws:'
    socket = new WebSocket(protocol + '//' + host + '/cyjl')
    $('#isconnect').addClass('hidden')
    $('#disconnect').addClass('hidden')
    $('#connecting').removeClass('hidden')
    $('#list').empty()
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
                    'length': $('#length').val(),
                    'noyd': ($('.button.active input[name="noyd"]').val() || 'False')
                }
                socket.send(JSON.stringify(init))
                $('#connect').attr('disabled', '')
                break
            case "disconnect":
                addToList('bg-reg', dict.msg)
                break
            case "connect":
                if (dict.youfirst) {
                    addToList('bg-green', '你先 :)')
                } else {
                    addToList('bg-red', '电脑先 :(')
                    addToList('', dict.output)
                    if (dict.extra) addToList('bg-mix', '电脑: ' + dict.extra)
                }
                $('#submit').removeAttr('disabled')
                $('#idiom').removeAttr('disabled')
                $('#connect').removeClass('bg-mix')
                $('#connect').removeClass('bg-red')
                $('#connect').addClass('bg-green')
                $('#isconnect').removeClass('hidden')
                $('#disconnect').addClass('hidden')
                $('#connecting').addClass('hidden')
                break
            case "msg":
                addToList('', '电脑: ' + dict.output)
                if (dict.extra) addToList('bg-mix', '电脑: ' + dict.extra)
                $('#submit').removeAttr('disabled')
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
        $('#disconnect').removeClass('hidden');
        $('#isconnect').addClass('hidden');
        $('#connecting').addClass('hidden');
        $('#connect').removeClass('bg-mix');
        $('#connect').removeClass('bg-green');
        $('#connect').addClass('bg-red');
        ismodeselect = false;
        $('#submit').attr('disabled', '');
        $('#idiom').attr('disabled', '');
        $('#connect').removeAttr('disabled')
    }
}