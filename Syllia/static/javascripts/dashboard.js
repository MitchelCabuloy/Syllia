var Dashboard = (function($, ko) {
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
        ko.applyBindings(new MODELS.DashboardModel(syllabusList), $("[data-slug='syllabus']")[0]);

        // Rubric
        var rubricList = [];

        $.each(jsonData.rubricList, function(index, value) {
            rubricList.push(new MODELS.ListItemModel(value));
        });
        ko.applyBindings(new MODELS.DashboardModel(rubricList), $("[data-slug='rubric']")[0]);

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

})(Zepto, ko);

var Profile = (function($, ko) {
    var MODULE = {}

    MODULE.init = function() {
        var viewModel = new MODELS.DropdownModel();
        ko.applyBindings(viewModel, $("[data-slug='user-profile']")[0])
        MODULE.bindUIActions();

        Foundation.libs.forms.refresh_custom_select($('#collegeSelect'), true);
        Foundation.libs.forms.refresh_custom_select($('#departmentSelect'), true);
    };

    MODULE.bindUIActions = function() {
        $("#btnProfileSubmit").click(function() {
            $("#profileForm").submit();
        });
    };

    var MODELS = (function() {
        var models = {}
        models.DropdownModel = function() {
            var self = this;
            self.college = ko.observable(window.jsonData.profileData.college);
            self.collegeList = ko.observableArray(window.jsonData.collegeList);

            self.department = ko.observable(window.jsonData.profileData.department);
            self.departmentList = ko.computed(function() {
                var tempList = [];

                $.each(window.jsonData.departmentList, function(index, value) {
                    if (value.college == self.college()) {
                        tempList.push(value);
                    }
                });

                return tempList;
            });
            self.college.subscribe(function() {
                Foundation.libs.forms.refresh_custom_select($('#departmentSelect'), true);
            });
        };

        return models;
    })();

    return MODULE;
})(Zepto, ko);

$(document).ready(function() {
    Dashboard.init();
    Profile.init();
});
