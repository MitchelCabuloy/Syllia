var jsonData = {
    syllabusList: [{
        pk: 1,
        url: "syllabus",
        itemName: "Test data 1",
        lastModified: "11:58 PM"
    }, {
        pk: 2,
        url: "syllabus",
        itemName: "Test data 2",
        lastModified: "11:58 PM"
    }, {
        pk: 3,
        url: "syllabus",
        itemName: "Test data 3",
        lastModified: "11:58 PM"
    }, {
        pk: 4,
        url: "syllabus",
        itemName: "Test data 4",
        lastModified: "11:58 PM"
    }, {
        pk: 5,
        url: "syllabus",
        itemName: "Test data 5",
        lastModified: "11:58 PM"
    }, {
        pk: 6,
        url: "syllabus",
        itemName: "Test data 6",
        lastModified: "11:58 PM"
    }, {
        pk: 7,
        url: "syllabus",
        itemName: "Test data 7",
        lastModified: "11:58 PM"
    }, {
        pk: 8,
        url: "syllabus",
        itemName: "Test data 8",
        lastModified: "11:58 PM"
    }, {
        pk: 9,
        url: "syllabus",
        itemName: "Test data 9",
        lastModified: "11:58 PM"
    }]
};

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

        // Change to rubricList once the serverside is implemented
        // $.each(jsonData.rubricList, function(index, value) {
        $.each(jsonData.syllabusList, function(index, value) {
            rubricList.push(new MODELS.ListItemModel(value));
        });
        ko.applyBindings(new MODELS.DashboardModel(rubricList), $("[data-slug='rubric']")[0]);

    };

    // Model declaration

    var MODELS = (function() {
        var models = {};

        models.DashboardModel = function(items) {
            var self = this;
            console.log(items);
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
            self.isSelected = ko.observable();
        };

        return models;
    })();

    return MODULE;

})(Zepto, ko);

$(document).ready(function() {
    Dashboard.init();
});
