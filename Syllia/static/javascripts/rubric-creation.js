var RubricModule = (function($, ko) {
    var MODULE = {}

    MODULE.init = function() {

        viewModel = new MODELS.RubricModel();
        ko.applyBindings(viewModel);
        MODULE.bindUIActions(viewModel);

        if ("jsonString" in window) {
            var jsonData = $.parseJSON(jsonString);
            this.loadData(viewModel, jsonData);
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
            $('#rubric_json').val(ko.toJSON(viewModel));
            $('#rubric_json_form').submit();
        });

        $('#stringifyBtn').click(function() {
            console.log("KO Data:");
            console.log(ko.toJSON(viewModel));
        });
    };

    var MODELS = (function() {
        var models = {};

        models.RubricModel = function() {
            var self = this;
            self.pk = null;
            self.rubricName = ko.observable();

            var criteriaObject = function() {
                this.criteriaName = "";
                this.exemplary = "";
                this.satisfactory = "";
                this.developing = "";
                this.beginning = "";
            };

            self.criterias = ko.observableArray([new criteriaObject()])

            self.addCriteria = function() {
                self.criterias.push(new criteriaObject());
            };

            self.removeCriteria = function(criteria) {
                self.criterias.remove(criteria);
            };
        };

        return models;

    })();

    return MODULE;

})(Zepto, ko);

$(document).ready(function() {
    RubricModule.init();
});
