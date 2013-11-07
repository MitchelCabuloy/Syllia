var Dashboard = (function($, ko, jsonData) {
    var MODULE = {};
    var PAGE_SIZE = 20;

    // Init method
    // public
    MODULE.init = function() {
        // Syllabus
        var syllabusList = [];

        $.each(jsonData.syllabusList, function(index, value) {
            syllabusList.push(new MODELS.ListItemModel(value));
        });
        var syllabusViewModel = new MODELS.DashboardModel(syllabusList, 'syllabus');
        ko.applyBindings(syllabusViewModel, $("[data-slug='syllabus']")[0]);

        // Rubric
        var rubricList = [];

        $.each(jsonData.rubricList, function(index, value) {
            rubricList.push(new MODELS.ListItemModel(value));
        });
        var rubricViewModel = new MODELS.DashboardModel(rubricList, 'rubric');
        ko.applyBindings(rubricViewModel, $("[data-slug='rubric']")[0]);

        MODULE.bindUIActions(syllabusViewModel);
        MODULE.bindUIActions(rubricViewModel);

    };

    MODULE.bindUIActions = function(viewModel) {
        $("#btnProfileSubmit").click(function() {
            $("#profileForm").submit();
        });

        $("#btnChangePasswordSubmit").click(function() {
            $('#change_password_form').submit();
        });

        // $(viewModel.context + " #btnDownload").click(function() {
        //     var item = viewModel.selectedItems()[0];
        //     $("#inputDownload").val(item.pk);
        //     $("#formDownload").submit();
        // });

        // $(viewModel.context + " #btnDelete").click(function() {
        //     // Do some stuff
        // });
    };

    MODULE.deleteData = function(viewModel) {
        var items = [];
        $.each(viewModel.selectedItems(), function(index, item) {
            items.push(parseInt(item.pk));
        });

        $.ajax({
            data: {
                ids_json: items
            },
            type: 'POST',
            url: '/' + viewModel.context + '/delete/',
            success: function(response) {
                console.log('Success delete');
                $.each(viewModel.selectedItems(), function(index, item) {
                    viewModel.listItems.remove(item);
                });
            },
            error: function(response) {
                console.log('Error delete');
            }
        });
    };

    // Model declaration

    var MODELS = (function() {
        var models = {};

        models.DashboardModel = function(items, context) {
            var self = this;
            self.context = context;
            self.btnDownload = $("[data-slug='" + self.context + "'] #btnDownload");
            self.btnDownloadAll = $("[data-slug='" + self.context + "'] #btnDownloadAll");
            self.btnDelete = $("[data-slug='" + self.context + "'] #btnDelete");
            self.selectCheck = $("[data-slug='" + self.context + "'] #multiSelector i.icon-check");
            self.selectMinus = $("[data-slug='" + self.context + "'] #multiSelector i.icon-check-minus");
            self.selectEmpty = $("[data-slug='" + self.context + "'] #multiSelector i.icon-check-empty");

            self.btnDownload.click(function() {
                var item = self.selectedItems()[0];
                $("#inputDownload").val(item.pk);
                $("#formDownload").submit();
            });

            self.btnDelete.click(function() {
                MODULE.deleteData(self);
            });

            var selectAction = function() {
                if (self.selectedItems().length == 0) {
                    $.each(self.pagedList(), function(index, item) {
                        item.isSelected(true);
                    });
                } else {
                    $.each(self.pagedList(), function(index, item) {
                        item.isSelected(false);
                    });
                }
            };

            $("[data-slug='" + self.context + "'] #multiSelector").click(selectAction);

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

            self.selectedItems.subscribe(function() {
                switch (self.selectedItems().length) {
                    case 0:
                        self.btnDownload.hide();
                        self.btnDownloadAll.hide();
                        self.btnDelete.hide();
                        break;
                    case 1:
                        self.btnDownload.show();
                        self.btnDownloadAll.hide();
                        self.btnDelete.show();
                        break;
                    default:
                        self.btnDownload.hide();
                        self.btnDownloadAll.show();
                        self.btnDelete.show();
                }

                if (self.selectedItems().length == self.listItems().length) {
                    self.selectCheck.show();
                    self.selectMinus.hide();
                    self.selectEmpty.hide();
                } else if (self.selectedItems().length != 0) {
                    self.selectCheck.hide();
                    self.selectMinus.show();
                    self.selectEmpty.hide();
                } else {
                    self.selectCheck.hide();
                    self.selectMinus.hide();
                    self.selectEmpty.show();
                }
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
