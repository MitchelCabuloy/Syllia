var RubricModule = (function($, ko) {
    var MODULE = {};

    MODULE.init = function() {

        var viewModel = new MODELS.RubricModel();
        ko.applyBindings(viewModel);
        MODULE.bindUIActions(viewModel);

        if ('jsonData' in window) {
            MODULE.loadData(viewModel, jsonData.rubricData);
            viewModel.timeSinceModified(jsonData.timeSinceModified);
        }
        $(document).foundation('abide', 'events');
    };

    MODULE.loadData = function(viewModel, json) {
        viewModel.pk = parseInt(json.pk);
        viewModel.rubricName(json.rubricName);
        viewModel.criterias(json.criterias);
    };

    MODULE.bindUIActions = function(viewModel) {
        $('#postBtn').click(function() {
            if (MODULE.isValid()) {
                var rubric_json = ko.toJSON(viewModel, function(key, value) {
                    switch (key) {
                        case "timeSinceModified":
                            return;
                        default:
                            return value;
                    }
                });

                $('#rubric_json').val(rubric_json);
                $('#rubric_json_form').submit();
            }
        });
    };

    MODULE.isValid = function() {
        var inputs = [];

        $('form[data-abide]').trigger('validate');
        inputs = $('input[data-invalid]');

        return inputs.length == 0 ? true : false;
    };
    var MODELS = (function() {
        var models = {};

        models.RubricModel = function() {
            var self = this;
            self.pk = null;
            self.rubricName = ko.observable();
            self.rubricName.subscribe(function() {
                document.title = self.rubricName() + " | Syllia";
            });
            self.criterias = ko.observableArray([new MODELS.CriteriaModel()]);
            self.timeSinceModified = ko.observable();

            self.addCriteria = function() {
                self.criterias.push(new MODELS.CriteriaModel());
                $(document).foundation('abide', 'events');
            };

            self.removeCriteria = function(criteria) {
                self.criterias.remove(criteria);
            };
        };

        models.CriteriaModel = function() {
            var self = this;
            self.criteriaName = "";
            self.exemplary = "";
            self.satisfactory = "";
            self.developing = "";
            self.beginning = "";
        };

        return models;

    })();

    return MODULE;

})(jQuery, ko);

$(document).ready(function() {
    RubricModule.init();
});
