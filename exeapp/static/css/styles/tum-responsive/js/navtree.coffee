$ ->
  show = (el) -> el.addClass("navshown").removeClass("navhidden")
  hide = (el) -> el.removeClass("navshown").addClass("navhidden")
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


  left.find("li").on "mouseover", (ev) ->
    show($(this).find("> ul"))
    show($(this).parents("ul"))
    update()

  left.find("li").on "mouseout", (ev) ->
    hide($(this).find("> ul"))
    update()

  $('#menu-toggle').click (e) ->
    e.preventDefault()
    $('body').toggleClass 'active'
    return