document.addEventListener('DOMContentLoaded', function () {
  new Splide('#image-slider', {
    fixedHeight: '60%',
    cover: true,
    autoplay: true,
    interval: 3000,
    rewind: true
  }).mount();
});
