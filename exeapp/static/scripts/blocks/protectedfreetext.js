var protectedfreetext = {
    init: function () {
        "use strict";
        $(document).ready(function () {
        });
    }
};

//''.join(chr(ord(k) ^ ord(c)) for c,k in zip(data, itertools.cycle(key)))

function disableEnterKey(elem, evnt)
{
    var key;
    var btn = $(elem).siblings(".pwd_freetext_btn");
    if(window.event)
        key = window.event.keyCode;     //IE
    else
        key = evnt.which;     //firefox
    if(key == 13)
    {
        pwdCheck(btn);
        return false;
    }
    else
        return true;
}

function xor_js(source, password) {
    var ret_ar = [],
        i, len,
        pwlen,
        pwindex = 0,
        s, p;
    if (typeof source === 'string') {
        source = source.split('');
    }
    if (Object.prototype.toString.call(source) === '[object Array]') {
        for (i = 0, len = source.length; i < len; ++i) {
            s = source[i];
            if (typeof s === 'string') {
                source[i] = s.charCodeAt(0);
            } else if (typeof s !== 'number') {
                console.log(s);
                throw ("Only str or [number, 'c', 'h',...] in xor \n Bad first param in function xor:" + s);
            }
        }
    } else {
        throw ('Very Bad first param in function xor:' + source);
    }
    if (typeof password === 'string') {
        password = password.split('');
    }
    if (Object.prototype.toString.call(password) === '[object Array]') {
        for (i = 0, len = password.length; i < len; ++i) {
            p = password[i];
            if (typeof p === 'string') {
                password[i] = p.charCodeAt(0);
            } else if (typeof p !== 'number') {
                console.log(p);
                throw ("Only str or [number, 'c', 'h',...] in xor \n Bad second param in function xor:" + p);
            }
        }
    } else {
        throw ('Very Bad second param in function xor:' + p);
    }
    pwlen = password.length;
    len = source.length;
    if (pwlen > 0) {
        for (i = 0; i < len; ++i) {
            ret_ar[i] = source[i] ^ password[i % pwlen]; // unefined ^7 === 7
        }
    } else {
        for (i = 0; i < len; ++i) {
            ret_ar[i] = ~source[i]; // ~unefined === -1
        }
    }
    source = password = i = pwlen = pwindex = null;
    return ret_ar.map(function(code) {
        return String.fromCharCode(code)
    }).join('');

}

function pwdCheck(elem)
{
    var password = $(elem).siblings(".pwd_for_protected_freetext").val();
    var content = $(elem).siblings(".protected_content").text();
    //$("#protected_content").remove();

    var plaintext = xor_js(decodeURI(content.trim()), password)
    plaintext = plaintext.trim();
    if(plaintext.match(/proof$/))
    {
        var index_of_proof = plaintext.lastIndexOf("proof");
        plaintext = plaintext.substring(0, index_of_proof);
        $(elem).siblings(".pwd_for_protected_freetext").remove();
        $(elem).siblings(".protected_freetext_hint").remove();
        $(elem).siblings(".protected_content").text('');
        $(elem).siblings(".protected_content").append(plaintext);
        $(elem).siblings(".protected_content").removeAttr( "style" );
        $(elem).remove();
    }
    else
    {
        $(elem).siblings(".protected_password_error").css("display", "inline");;
        $(elem).siblings(".protected_password_error").fadeIn().delay(1500).fadeOut();
    }
    //console.log(decodeURI(content));
    //console.log(password);
    //console.log(xor_js(decodeURI(content), password));
}

if (typeof(requirejs) !== "undefined") {
    define("protectedfreetext", ['jquery'], function ($) {
        return protectedfreetext;
    })
} else {
    protectedfreetext.init();
}
