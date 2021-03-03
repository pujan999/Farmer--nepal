/*!
 * Start Bootstrap - SB Admin 2 v4.1.3 (https://startbootstrap.com/theme/sb-admin-2)
 * Copyright 2013-2020 Start Bootstrap
 * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin-2/blob/master/LICENSE)
 */

!(function (s) {
  'use strict';
  s('#sidebarToggle, #sidebarToggleTop').on('click', function (e) {
    s('body').toggleClass('sidebar-toggled'),
      s('.sidebar').toggleClass('toggled'),
      s('.sidebar').hasClass('toggled') &&
        s('.sidebar .collapse').collapse('hide');
  }),
    s(window).resize(function () {
      s(window).width() < 768 && s('.sidebar .collapse').collapse('hide'),
        s(window).width() < 480 &&
          !s('.sidebar').hasClass('toggled') &&
          (s('body').addClass('sidebar-toggled'),
          s('.sidebar').addClass('toggled'),
          s('.sidebar .collapse').collapse('hide'));
    }),
    s('body.fixed-nav .sidebar').on(
      'mousewheel DOMMouseScroll wheel',
      function (e) {
        if (768 < s(window).width()) {
          var o = e.originalEvent,
            l = o.wheelDelta || -o.detail;
          (this.scrollTop += 30 * (l < 0 ? 1 : -1)), e.preventDefault();
        }
      }
    ),
    s(document).on('scroll', function () {
      100 < s(this).scrollTop()
        ? s('.scroll-to-top').fadeIn()
        : s('.scroll-to-top').fadeOut();
    }),
    s(document).on('click', 'a.scroll-to-top', function (e) {
      var o = s(this);
      s('html, body')
        .stop()
        .animate(
          { scrollTop: s(o.attr('href')).offset().top },
          1e3,
          'easeInOutExpo'
        ),
        e.preventDefault();
    });
})(jQuery);

const $tableID = $('#table');
const $BTN = $('#export-btn');
const $EXPORT = $('#export');

const newTr = `
<tr class="hide">
  <td class="pt-3-half" contenteditable="true">Example</td>
  <td class="pt-3-half" contenteditable="true">Example</td>
  <td class="pt-3-half" contenteditable="true">Example</td>
  <td class="pt-3-half" contenteditable="true">Example</td>
  <td class="pt-3-half" contenteditable="true">Example</td>
  <td class="pt-3-half">
    <span class="table-up"><a href="#!" class="indigo-text"><i class="fas fa-long-arrow-alt-up" aria-hidden="true"></i></a></span>
    <span class="table-down"><a href="#!" class="indigo-text"><i class="fas fa-long-arrow-alt-down" aria-hidden="true"></i></a></span>
  </td>
  <td>
    <span class="table-remove"><button type="button" class="btn btn-danger btn-rounded btn-sm my-0 waves-effect waves-light">Remove</button></span>
  </td>
</tr>`;

$('.table-add').on('click', 'i', () => {
  const $clone = $tableID
    .find('tbody tr')
    .last()
    .clone(true)
    .removeClass('hide table-line');

  if ($tableID.find('tbody tr').length === 0) {
    $('tbody').append(newTr);
  }

  $tableID.find('table').append($clone);
});

$tableID.on('click', '.table-remove', function () {
  $(this).parents('tr').detach();
});

$tableID.on('click', '.table-up', function () {
  const $row = $(this).parents('tr');

  if ($row.index() === 0) {
    return;
  }

  $row.prev().before($row.get(0));
});

$tableID.on('click', '.table-down', function () {
  const $row = $(this).parents('tr');
  $row.next().after($row.get(0));
});

// A few jQuery helpers for exporting only
jQuery.fn.pop = [].pop;
jQuery.fn.shift = [].shift;

$BTN.on('click', () => {
  const $rows = $tableID.find('tr:not(:hidden)');
  const headers = [];
  const data = [];

  // Get the headers (add special header logic here)
  $($rows.shift())
    .find('th:not(:empty)')
    .each(function () {
      headers.push($(this).text().toLowerCase());
    });

  // Turn all existing rows into a loopable array
  $rows.each(function () {
    const $td = $(this).find('td');
    const h = {};

    // Use the headers from earlier to name our hash keys
    headers.forEach((header, i) => {
      h[header] = $td.eq(i).text();
    });

    data.push(h);
  });

  // Output the result
  $EXPORT.text(JSON.stringify(data));
});
