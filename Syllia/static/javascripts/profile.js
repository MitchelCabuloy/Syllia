var Profile = (function($, ko) {
    var MODULE = {}

    MODULE.init = function() {
        var viewModel = new MODELS.DropdownModel();
        ko.applyBindings(viewModel, $("[data-slug='user-profile']")[0])

        Foundation.libs.forms.refresh_custom_select($('#collegeSelect'), true);
        Foundation.libs.forms.refresh_custom_select($('#departmentSelect'), true);
    };

    var MODELS = (function() {
        var models = {}
        models.DropdownModel = function() {
            var self = this;
            self.college = ko.observable();

            if (window.jsonData.profileData)
                self.college(window.jsonData.profileData.college);

            self.collegeList = ko.observableArray(window.jsonData.collegeList);

            self.department = ko.observable();

            if (window.jsonData.profileData)
                self.department(window.jsonData.profileData.department);

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
    Profile.init();
});
