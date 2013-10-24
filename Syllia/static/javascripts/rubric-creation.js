(function() {
    var viewModel,
        RubricModel,
        RubricModule = {
            init: function() {
                this.bindUIActions();
                this.defineModels();

                viewModel = new RubricModel();

                ko.applyBindings(viewModel);

                if ("jsonString" in window) {
                    var jsonData = $.parseJSON(jsonString);
                    this.loadData(jsonData);
                } else {
                    // Uncomment for test data
                    // this.loadData($.parseJSON('{"pk":null,"rubricName":"NTCOR04 Rubric AY 2013-2015","criterias":[{"criteriaName":"Equipment and Resources","exemplary":"Exemplary lorem ipsum","satisfactory":"Satisfactory lorem ipsum","developing":"Developing lorem ipsum","beginning":"Beginning lorem ipsum"},{"criteriaName":"Second Criteria","exemplary":"Exemplary ipsum lorem","satisfactory":"Satisfactory ipsum lorem","developing":"Developing ipsum lorem","beginning":"Beginning ipsum lorem"}]}'));
                }
            },

            defineModels: function() {
                RubricModel = function() {
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
            },

            loadData: function(json) {
                viewModel.pk = parseInt(json.pk)
                viewModel.rubricName(json.rubricName)
                viewModel.criterias(json.criterias)
            },

            bindUIActions: function() {
                $('#postBtn').click(function() {
                    $('#rubric_json').val(ko.toJSON(viewModel));
                    $('#rubric_json_form').submit();
                });

                $('#stringifyBtn').click(function() {
                    console.log("KO Data:");
                    console.log(ko.toJSON(viewModel));
                });
            }
        };

    $(document).ready(function() {
        RubricModule.init();
    });
})();
