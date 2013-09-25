var viewModel,
    SyllabusModel,
    ElgaModel,
    LearningPlanModel,
    SyllabusModule = {
        init: function() {
            this.bindUIActions();
            this.defineModels();

            viewModel = new SyllabusModel();

            ko.applyBindings(viewModel);

            if ("jsonString" in window) {
                var jsonData = $.parseJSON(jsonString);
                this.loadData(jsonData);
            }
        },

        defineModels: function() {
            SyllabusModel = function() {
                var self = this;
                self.college = "";
                self.department = "";
                self.courseCode = "";
                self.courseName = "";
                self.courseDescription = "";


                var schedule = function() {
                    this.days = "";
                    this.startTime = "";
                    this.endTime = "";
                };

                self.schedules = ko.observableArray([new schedule()]);

                self.addSchedule = function() {
                    self.schedules.push(new schedule());
                };

                self.removeSchedule = function(schedule) {
                    self.schedules.remove(schedule);
                };


                self.instructors = ko.observableArray([{
                    firstName: ko.observable(),
                    lastName: ko.observable()
                }]);

                self.addInstructor = function() {
                    self.instructors.push({
                        firstName: ko.observable(),
                        lastName: ko.observable()
                    });
                };

                self.removeInstructor = function(instructor) {
                    self.instructors.remove(instructor);
                };


                self.elgas = ko.observableArray([new ElgaModel()]);

                self.addElga = function() {
                    self.elgas.push(new ElgaModel());
                };

                self.removeElga = function(elga) {
                    self.elgas.remove(elga);
                };


                self.finalCourseOutputDescription = ko.observable();
                self.requiredOutputs = ko.observableArray([{
                    description: ko.observable(),
                    weekDue: ko.observable(),
                    los: ko.observableArray()
                }]);

                self.addRequiredOutput = function() {
                    self.requiredOutputs.push({
                        description: ko.observable(),
                        weekDue: ko.observable(),
                        los: ko.observableArray()
                    });
                };

                self.removeRequiredOutput = function(requiredOutput) {
                    self.requiredOutputs.remove(requiredOutput);
                };


                self.otherOutputs = ko.observableArray([{
                    requirementName: ko.observable()
                }]);

                self.addOtherOutput = function() {
                    self.otherOutputs.push({
                        requirementName: ko.observable()
                    });
                };

                self.removeOtherOutput = function(otherOutput) {
                    self.otherOutputs.remove(otherOutput);
                };


                self.gradingSystems = ko.observableArray([{
                    itemName: ko.observable(),
                    percentage: ko.observable()
                }]);

                self.addGradingSystem = function() {
                    self.gradingSystems.push({
                        itemName: ko.observable(),
                        percentage: ko.observable()
                    });
                };

                self.removeGradingSystem = function(gradingSystem) {
                    self.gradingSystems.remove(gradingSystem);
                };

                self.totalGradingSystem = ko.computed(function() {
                    var gradingSystems = self.gradingSystems();
                    var total = 0;
                    $.each(gradingSystems, function(index, item) {
                        var temp = parseInt(item.percentage);
                        if (!isNaN(temp))
                            total += temp;
                    });

                    return total;
                })


                self.learningPlans = ko.observableArray([new LearningPlanModel()]);

                self.addLearningPlan = function() {
                    self.learningPlans.push(new LearningPlanModel());
                };

                self.removeLearningPlan = function(learningPlan) {
                    self.learningPlans.remove(learningPlan);
                };


                self.references = ko.observableArray([{
                    referenceText: ko.observable()
                }]);

                self.addReference = function() {
                    self.references.push({
                        referenceText: ko.observable()
                    });
                };

                self.removeReference = function(reference) {
                    self.references.remove(reference);
                };


                self.classPolicies = ko.observableArray([{
                    policy: ko.observable()
                }]);

                self.addClassPolicy = function() {
                    self.classPolicies.push({
                        policy: ko.observable()
                    });
                };

                self.removeClassPolicy = function(policy) {
                    self.classPolicies.remove(policy);
                };

            };

            ElgaModel = function() {
                var self = this;
                self.elgaName = ko.observable();
                self.learningOutcomes = ko.observableArray([{
                    description: ko.observable()
                }]);

                self.addLearningOutcome = function() {
                    self.learningOutcomes.push({
                        description: ko.observable()
                    });
                };

                self.removeLearningOutcome = function(lo) {
                    self.learningOutcomes.remove(lo);
                };
            };

            LearningPlanModel = function() {
                var self = this;
                self.topic = ko.observable();
                self.weekNumber = ko.observable();
                self.learningActivities = ko.observableArray([{
                    description: ko.observable()
                }]);
                self.los = ko.observableArray();

                self.addLearningActivity = function() {
                    self.learningActivities.push({
                        description: ko.observable()
                    });
                };

                self.removeLearningActivity = function(learningActivity) {
                    self.learningActivities.remove(learningActivity);;
                };

            };
        },

        loadData: function(json) {
            viewModel.college(json.college);
            viewModel.department(json.department);
            viewModel.courseCode(json.courseCode);
            viewModel.courseName(json.courseName);
            viewModel.courseDescription(json.courseDescription);
            viewModel.schedules(json.schedules);
            viewModel.instructors(json.instructors);

            viewModel.elgas.removeAll();
            $.each(json.elgas, function(index, data) {
                elga = new ElgaModel();

                elga.elgaName(data.elgaName);

                elga.learningOutcomes.removeAll();
                $.each(data.learningOutcomes, function(index, lo) {
                    elga.learningOutcomes.push({
                        description: ko.observable(lo.description)
                    });
                });

                viewModel.elgas.push(elga);
            });

            viewModel.finalCourseOutputDescription(json.finalCourseOutputDescription);
            viewModel.requiredOutputs(json.requiredOutputs);
            viewModel.otherOutputs(json.otherOutputs);
            viewModel.gradingSystems(json.gradingSystems);

            viewModel.learningPlans.removeAll();
            $.each(json.learningPlans, function(index, data) {
                lp = new LearningPlanModel();

                lp.topic(data.topic);
                lp.weekNumber(data.weekNumber);
                lp.learningActivities(data.learningActivities);
                lp.los(data.los);

                viewModel.learningPlans.push(lp);
            });

            viewModel.references(json.references);
            viewModel.classPolicies(json.classPolicies);
        },

        bindUIActions: function() {
            $('#postBtn').click(function() {
                $("#syllabus_json").val(ko.toJSON(viewModel));
                $("form").submit();
            });

            $('#stringifyBtn').click(function() {
                console.log(ko.toJSON(viewModel));
            });
        }
    };


$(document).ready(function() {
    SyllabusModule.init();
});
