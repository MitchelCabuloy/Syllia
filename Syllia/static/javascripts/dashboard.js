var Dashboard = (function($, ko, jsonData) {
    var MODULE = {};
    var PAGE_SIZE = 5;

    // Init method
    // public
    MODULE.init = function() {
        // Syllabus
        var syllabusList = [];

        $.each(jsonData.syllabusList, function(index, value) {
            syllabusList.push(new MODELS.ListItemModel(value));
        });
        var syllabusViewModel = new MODELS.DashboardModel(syllabusList);
        ko.applyBindings(syllabusViewModel, $("[data-slug='syllabus']")[0]);

        // Rubric
        var rubricList = [];

        $.each(jsonData.rubricList, function(index, value) {
            rubricList.push(new MODELS.ListItemModel(value));
        });
        ko.applyBindings(new MODELS.DashboardModel(rubricList), $("[data-slug='rubric']")[0]);

        MODULE.bindUIActions(syllabusViewModel);

    };

    MODULE.bindUIActions = function(syllabusViewModel) {
        $("#btnProfileSubmit").click(function() {
            $("#profileForm").submit();
        });

        $("#btnChangePasswordSubmit").click(function() {
            $('#change_password_form').submit();
        });

        $("#btnDownload").click(function() {
            var item = syllabusViewModel.selectedItems()[0];
            $("#inputDownload").val(item.pk);
            $("#formDownload").submit();
        });
    };

    // Model declaration

    var MODELS = (function() {
        var models = {};

        models.DashboardModel = function(items) {
            var self = this;
            self.listItems = ko.observableArray(items);

            self.pageIndex = ko.observable(1);
            self.pagedList = ko.computed(function() {
                var startIndex = (self.pageIndex() - 1) * PAGE_SIZE;
                var endIndex = startIndex + PAGE_SIZE;
                return self.listItems().slice(startIndex, endIndex);
            }, self);

            self.selectedItems = ko.computed(function() {
                var items = [];

                $.each(self.listItems(), function(index, item) {
                    if (item.isSelected()) {
                        items.push(item);
                    }
                });

                return items;
            });

            // TODO: Disable buttons on first and last pages.
            self.nextPage = function() {
                self.pageIndex(self.pageIndex() + 1);
            };

            self.previousPage = function() {
                self.pageIndex(self.pageIndex() - 1);
            };

            self.hasMoreThanOnePage = ko.computed(function() {
                return self.listItems().length / PAGE_SIZE >= 1 ? true : false;
            }, self);
        };

        models.ListItemModel = function(value) {
            var self = this;
            // Quotes for static things
            self.pk = value.pk;
            self.itemName = value.itemName;
            self.lastModified = value.lastModified;
            self.url = "/" + value.url + "/" + value.pk;

            // Observables for things that change
            self.isSelected = ko.observable(false);

            self.select = function(data, event) {
                if (event.target.tagName != "INPUT") {
                    window.location.href = data.url;
                }

                return true;
            };
        };

        return models;
    })();

    return MODULE;

})(Zepto, ko, jsonData);

$(document).ready(function() {
    Dashboard.init();
});
