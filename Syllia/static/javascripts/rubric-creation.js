(function() {
    var viewModel,
        RubricModel,
        RubricModule = {
            init: function() {
                this.bindUIActions();
                this.defineModels();

                viewModel = new RubricModel();

                ko.applyBindings(viewModel);
            },

            defineModels: function() {
                RubricModel = function() {
                    var self = this;
                    self.rubricName = "";

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

            bindUIActions: function() {
                $('#postBtn').click(function() {
                    $('#rubric_json').val(ko.toJSON(viewModel));
                    $('#rubric_json_form').submit();
                });
            }
        };

    $(document).ready(function() {
        RubricModule.init();
    });
})();