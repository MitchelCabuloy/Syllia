var RubricModule = (function($, ko) {
    var MODULE = {}

    MODULE.init = function() {

        viewModel = new MODELS.RubricModel();
        ko.applyBindings(viewModel);
        MODULE.bindUIActions(viewModel);

        if (jsonData.rubricData) {
            MODULE.loadData(viewModel, jsonData.rubricData);
            viewModel.timeSinceModified(jsonData.timeSinceModified);
        } else {
            // Uncomment for test data
            // this.loadData($.parseJSON('{"pk":null,"rubricName":"NTCOR04 Rubric AY 2013-2015","criterias":[{"criteriaName":"Equipment and Resources","exemplary":"Exemplary lorem ipsum","satisfactory":"Satisfactory lorem ipsum","developing":"Developing lorem ipsum","beginning":"Beginning lorem ipsum"},{"criteriaName":"Second Criteria","exemplary":"Exemplary ipsum lorem","satisfactory":"Satisfactory ipsum lorem","developing":"Developing ipsum lorem","beginning":"Beginning ipsum lorem"}]}'));
        }
    };

    MODULE.loadData = function(viewModel, json) {
        viewModel.pk = parseInt(json.pk)
        viewModel.rubricName(json.rubricName)
        viewModel.criterias(json.criterias)
    };

    MODULE.bindUIActions = function(viewModel) {
        $('#postBtn').click(function() {
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
        });

        $('#stringifyBtn').click(function() {
            var rubric_json = ko.toJSON(viewModel, function(key, value) {
                switch (key) {
                    case "timeSinceModified":
                        return;
                    default:
                        return value;
                }
            });

            console.log("KO Data:");
            console.log(rubric_json);
        });
    };

    var MODELS = (function() {
        var models = {};

        models.RubricModel = function() {
            var self = this;
            self.pk = null;
            self.rubricName = ko.observable();
            self.criterias = ko.observableArray([new models.CriteriaModel()])
            self.timeSinceModified = ko.observable();

            self.addCriteria = function() {
                self.criterias.push(new models.criteriaObject());
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

})(Zepto, ko);

$(document).ready(function() {
    RubricModule.init();
});
