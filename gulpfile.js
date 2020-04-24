var gulp = require('gulp'),
    concatCSS = require('gulp-concat-css'),
    prefixer =require('gulp-autoprefixer'),
    minifyCSS = require('gulp-minify-css'),
    rename = require('gulp-rename');



function css_builder() {
  return gulp.src('static/css/_css/*.css')
  .pipe(concatCSS('main.css'))
  .pipe(prefixer())
  .pipe(minifyCSS())
  .pipe(rename({suffix: '.min'}))
  .pipe(gulp.dest('app/Qmblog/static/css/'))
};

function watch() {
  gulp.watch('static/css/_css/*.css', css_builder)
}

gulp.task('start', watch)
