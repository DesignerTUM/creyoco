$ ->
  show = (el) ->
    el.addClass("navshown").removeClass("navhidden")
  hide = (el) ->
    el.removeClass("navshown").addClass("navhidden")
  lastTimeout = undefined
  update = () ->
    clearTimeout(lastTimeout)
    lastTimeout = setTimeout(
      (() ->
        $(".navshown").slideDown()
        $(".navhidden:not(.neverhide)").slideUp()
      ), 200
    )


  left = $("aside.left > nav")
  hide(left.find("ul > li > ul").hide())
  active = left.find(".active").parent()
  active.show().addClass("neverhide")
  active.find("> li, > ul").show().addClass("neverhide")
  active.parents("ul").show().addClass("neverhide")

  debounce= (func, threshold, execAsap) ->
    timeout = null
    (args...) ->
      obj = this
      delayed = ->
        func.apply(obj, args) unless execAsap
        timeout = null
      if timeout
        clearTimeout(timeout)
      else if (execAsap)
        func.apply(obj, args)
      timeout = setTimeout delayed, threshold || 100

  narrow = debounce((->
    left.find("li").off()
    left.find()
    a_list = $(".left").find("ul").not(".neverhide").parent().children("a")
    a_list.each ->
      a = $(this)
      url_text = a.html()
      if url_text.indexOf("</span>") == -1
        a.html url_text + '<span class=\'glyphicon glyphicon-chevron-down\'></span>'
      return

    $('.left .glyphicon').off('click')
    $('.left .glyphicon').on 'click', (e) ->
      e.preventDefault()
      if $(this).hasClass('glyphicon-chevron-down')
        $(this).removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
        parent = $(this).parent().parent()
        show(parent.find("> ul"))
        show(parent.parents("ul"))
        update()
      else if $(this).hasClass('glyphicon-chevron-up')
        $(this).removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')
        parent = $(this).parent().parent()
        hide(parent.find("> ul"))
        update()


    menu_toggle = $('#menu-toggle')
    menu_toggle.off()
    menu_toggle.click (e) ->
      e.preventDefault()
      $('body').toggleClass 'active'
      return
    ),500)

  wide = debounce((->
    left.find("span.glyphicon").remove()
    left.find("li").on "mouseover", (ev) ->
      show($(this).find("> ul"))
      show($(this).parents("ul"))
      update()

    left.find("li").on "mouseout", (ev) ->
      hide($(this).find("> ul"))
      update()
      ),500)


  $(window).on 'resize', ->
    if $(this).width() > 767
      wide()
    else
      narrow()

  if $(window).width() > 767
    wide()
  else
    narrow()


