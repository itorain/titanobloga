module.exports = function (grunt) {
    'use strict';
    grunt.initConfig({
        concat: {
            dist: {
                src: [
                    'blog/static/blog/css/bulma.css',
                    'blog/static/blog/css/custom.css',
                    'blog/static/blog/css/stars.css',
                    'blog/static/blog/css/code_highlighting.css',
                ],
                dest: 'blog/static/css/style.css'
            }
        },
        cssmin: {
            dist: {
                src: 'blog/static/css/style.css',
                dest: 'blog/static/blog/css/style.min.css'
            }
        }
    });
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.registerTask('default', ['concat', 'cssmin']);
};
