var jsonData = {
    syllabusList: [{
        pk: 1,
        itemName: "Test data 1",
        lastModified: "11:58 PM"
    }, {
        pk: 2,
        itemName: "Test data 2",
        lastModified: "11:58 PM"
    }, {
        pk: 3,
        itemName: "Test data 3",
        lastModified: "11:58 PM"
    }, {
        pk: 4,
        itemName: "Test data 4",
        lastModified: "11:58 PM"
    }, {
        pk: 5,
        itemName: "Test data 5",
        lastModified: "11:58 PM"
    }, {
        pk: 6,
        itemName: "Test data 6",
        lastModified: "11:58 PM"
    }, {
        pk: 7,
        itemName: "Test data 7",
        lastModified: "11:58 PM"
    }, {
        pk: 8,
        itemName: "Test data 8",
        lastModified: "11:58 PM"
    }, {
        pk: 9,
        itemName: "Test data 9",
        lastModified: "11:58 PM"
    }, {
        pk: 10,
        itemName: "Test data 10",
        lastModified: "11:58 PM"
    }]
};

var Dashboard = (function($, ko) {
    var MODULE = {};
    var PAGE_SIZE = 5;

    // Init method
    MODULE.init = function() {
        // Syllabus
        var syllabusList = [];

        $.each(jsonData.syllabusList, function(index, value) {
            syllabusList.push(new MODELS.ListItemModel(value.itemName, value.lastModified));
        });
        // ko.applyBindings(new MODELS.DashboardModel(syllabusList));
        ko.applyBindings(new MODELS.DashboardModel(syllabusList), $("[data-slug='syllabus']")[0]);

    };

    // Model declaration
    var MODELS = (function Models() {
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


            self.nextPage = function() {
                self.pageIndex(self.pageIndex() + 1);
            };

            self.previousPage = function() {
                self.pageIndex(self.pageIndex() - 1);
            };
        };

        models.ListItemModel = function(itemName, lastModified) {
            var self = this;
            // Quotes for static things
            self.itemName = itemName;
            self.lastModified = lastModified;

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
