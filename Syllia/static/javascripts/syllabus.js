var SyllabusModule = (function($, ko) {
    var MODULE = {};

    MODULE.init = function() {
        var viewModel = new MODELS.SyllabusModel();
        viewModel.errors = ko.validation.group(viewModel, {
            deep: true
        });

        // ko.applyBindings(viewModel);
        ko.applyBindingsWithValidation(viewModel);
        MODULE.bindUIActions(viewModel);

        if (jsonData.syllabusData) {
            // var jsonData = $.parseJSON(jsonString);
            MODULE.loadData(viewModel, jsonData.syllabusData);
            viewModel.timeSinceModified(jsonData.timeSinceModified);
        } else {
            // Uncomment for test data
            // this.loadData($.parseJSON('{"college":"College of Computer Studies","department":"Computer Technology","courseCode":"LBYFORE","courseName":"LBYFORE","courseDescription":"LBYFORE is a course that is the hands-on laboratory component of FORENSC.","schedules":[{"endTime":"1740","days":"S","startTime":"1440"},{"endTime":"1600","days":"TH","startTime":"1300"}],"instructors":[{"fullName":"Alexis Pantola"},{"fullName":"Gregory Cu"}],"elgas":[{"elgaName":"Effective Communicator","learningOutcomes":[{"description":"LO 1: Be able to discuss different digital blah."}]},{"elgaName":"Critical/creative thinker","learningOutcomes":[{"description":"LO 2: Be able to gather artifact from different blah"},{"description":"LO 3: Be able to gather artifact from different operating systems"}]}],"finalCourseOutputDescription":"Final course output description here","requiredOutputs":[{"los":["LO 1: Be able to discuss different digital blah."],"description":"Forensic Platform Preparation Report","weekDue":"4"},{"los":["LO 2: Be able to gather artifact from different blah","LO 3: Be able to gather artifact from different operating systems"],"description":"Windows System and Artifacts Report","weekDue":"5"}],"otherOutputs":[{"requirementName":"Laboratory Exam"},{"requirementName":"Group Project"}],"gradingSystems":[{"percentage":"60","itemName":"Laboratory Report Average"},{"percentage":"20","itemName":"Group Project"},{"percentage":"20","itemName":"Laboratory Exam"}],"totalGradingSystem":100,"learningPlans":[{"topic":"Introduction / Orientation","weekNumber":"1","learningActivities":[{"description":"Course introduction"},{"description":"Classroom policies discussion"}],"los":[]},{"topic":"1.0 Forensic Platform Preparation","weekNumber":"3","learningActivities":[{"description":"Hands-on"}],"los":["LO 1: Be able to discuss different digital blah."]},{"topic":"2.0 Windows Systems and Artifacts","weekNumber":"4","learningActivities":[{"description":"Hands-on"}],"los":["LO 2: Be able to gather artifact from different blah","LO 3: Be able to gather artifact from different operating systems"]}],"references":[{"referenceText":"Reference, First"},{"referenceText":"Reference, Second"},{"referenceText":"Reference, Third"},{"referenceText":"Test reference. Saved from shell."}],"classPolicies":[{"policy":"No eating"},{"policy":"No cheating"}]}'));
        }

        Foundation.libs.forms.refresh_custom_select($('#collegeSelect'), true);
        Foundation.libs.forms.refresh_custom_select($('#departmentSelect'), true);
        Foundation.libs.forms.refresh_custom_select($('#rubricSelect'), true);
    };

    MODULE.loadData = function(viewModel, json) {
        viewModel.pk = parseInt(json.pk);
        viewModel.syllabusName(json.syllabusName);
        viewModel.college(json.college);
        viewModel.department(json.department);
        viewModel.courseCode(json.courseCode);
        viewModel.courseName(json.courseName);
        viewModel.courseDescription(json.courseDescription);
        viewModel.schedules(json.schedules);
        viewModel.instructors(json.instructors);
        viewModel.rubric(json.rubric);

        viewModel.elgas.removeAll();
        $.each(json.elgas, function(index, data) {
            elga = new MODELS.ElgaModel();

            // elga.pk = parseInt(data.pk)
            elga.elgaName(data.elgaName);

            elga.learningOutcomes.removeAll();
            $.each(data.learningOutcomes, function(index, lo) {
                elga.learningOutcomes.push({
                    // pk: parseInt(lo.pk),
                    description: ko.observable(lo.description)
                });
            });

            viewModel.elgas.push(elga);
        });

        viewModel.finalCourseOutputDescription(json.finalCourseOutputDescription);
        viewModel.requiredOutputs(json.requiredOutputs);
        viewModel.otherOutputs(json.otherOutputs);
        // TODO: Create array of GradingSystemModel() objects instead of passing directly

        var tempList = [];
        $.each(json.gradingSystems, function(index, value) {
            var tempItem = new MODELS.GradingSystemModel();
            tempItem.itemName(value.itemName);
            tempItem.percentage(value.percentage);
            tempList.push(tempItem);
        });

        viewModel.gradingSystems(tempList);

        viewModel.learningPlans.removeAll();
        $.each(json.learningPlans, function(index, data) {
            lp = new MODELS.LearningPlanModel();

            // lp.pk = parseInt(data.pk)
            lp.topic(data.topic);
            lp.weekNumber(data.weekNumber);
            lp.learningActivities(data.learningActivities);
            lp.los(data.los);

            viewModel.learningPlans.push(lp);
        });

        viewModel.references(json.references);
        viewModel.classPolicies(json.classPolicies);
    };

    MODULE.bindUIActions = function(viewModel) {
        $('#postBtn').click(function() {
            // Ignores these fields
            var syllabus_json = ko.toJSON(viewModel, function(key, value) {
                switch (key) {
                    case "collegeList":
                    case "departmentList":
                    case "rubricList":
                    case "timeSinceModified":
                        return;
                    default:
                        return value;
                }
            });

            $('#syllabus_json').val(syllabus_json);
            $('#syllabus_json_form').submit();
        });

        $('#stringifyBtn').click(function() {
            // Ignores these fields
            var syllabus_json = ko.toJSON(viewModel, function(key, value) {
                switch (key) {
                    case "collegeList":
                    case "departmentList":
                    case "rubricList":
                    case "timeSinceModified":
                        return;
                    default:
                        return value;
                }
            });

            console.log("KO Data:");
            console.log(syllabus_json);
        });

        $('#validateBtn').click(function() {
            console.log('Validating...');
            viewModel.errors = ko.validation.group(viewModel, {
                deep: true
            });
            viewModel.errors.showAllMessages();
        });
    };

    var MODELS = (function() {
        var models = {};
        models.SyllabusModel = function() {
            var self = this;
            self.pk = null;
            self.syllabusName = ko.observable().extend({
                required: true
            });
            self.courseCode = ko.observable().extend({
                required: true
            });
            self.courseName = ko.observable().extend({
                required: true
            });
            self.courseDescription = ko.observable().extend({
                required: true
            });
            self.timeSinceModified = ko.observable();

            // Dropdown lists
            self.college = ko.observable();
            self.collegeList = ko.observableArray(window.jsonData.collegeList);

            self.department = ko.observable();
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

            self.rubric = ko.observable();
            self.rubricList = ko.observableArray(window.jsonData.rubricList);

            self.schedules = ko.observableArray([new MODELS.ScheduleModel()]);
            self.addSchedule = function() {
                self.schedules.push(new MODELS.ScheduleModel());
            };
            self.removeSchedule = function(schedule) {
                self.schedules.remove(schedule);
            };

            self.instructors = ko.observableArray([new MODELS.InstructorModel()]);
            self.addInstructor = function() {
                self.instructors.push(new MODELS.InstructorModel());
            };
            self.removeInstructor = function(instructor) {
                self.instructors.remove(instructor);
            };

            self.elgas = ko.observableArray();
            self.addElga = function() {
                var elga = new MODELS.ElgaModel(self.elgas().length + 1)
                self.elgas.push(elga);
            };
            self.removeElga = function(elga) {
                $.each(self.elgas(), function(index, elgaTemp) {
                    if (elga.learningOutcomeNumber() < elgaTemp.learningOutcomeNumber()) {
                        elgaTemp.learningOutcomeNumber(elgaTemp.learningOutcomeNumber() - 1);
                    }
                });

                self.elgas.remove(elga);
            };
            self.addElga();

            self.finalCourseOutputDescription = ko.observable().extend({
                required: true
            });

            self.requiredOutputs = ko.observableArray([new MODELS.RequiredOutputModel()]);
            self.addRequiredOutput = function() {
                self.requiredOutputs.push(new MODELS.RequiredOutputModel());
            };
            self.removeRequiredOutput = function(requiredOutput) {
                self.requiredOutputs.remove(requiredOutput);
            };


            self.otherOutputs = ko.observableArray([new MODELS.OtherOutputModel()]);
            self.addOtherOutput = function() {
                self.otherOutputs.push(new MODELS.OtherOutputModel());
            };
            self.removeOtherOutput = function(otherOutput) {
                self.otherOutputs.remove(otherOutput);
            };

            // TODO: Rename this variable
            self.gradingSystems = ko.observableArray([new MODELS.GradingSystemModel()]);
            self.addGradingSystem = function() {
                self.gradingSystems.push(new MODELS.GradingSystemModel());
            };
            self.removeGradingSystem = function(gradingSystem) {
                self.gradingSystems.remove(gradingSystem);
            };
            self.totalGradingSystem = ko.computed(function() {
                var gradingSystems = self.gradingSystems();
                var total = 0;
                $.each(gradingSystems, function(index, item) {
                    var temp = parseInt(item.percentage())
                    if (!isNaN(temp))
                        total += temp;
                });

                return total;
            });


            self.learningPlans = ko.observableArray([new MODELS.LearningPlanModel()]);
            self.addLearningPlan = function() {
                self.learningPlans.push(new MODELS.LearningPlanModel());
            };
            self.removeLearningPlan = function(learningPlan) {
                self.learningPlans.remove(learningPlan);
            };

            self.references = ko.observableArray([new MODELS.ReferenceModel()]);
            self.addReference = function() {
                self.references.push(new MODELS.ReferenceModel());
            };
            self.removeReference = function(reference) {
                self.references.remove(reference);
            };

            self.classPolicies = ko.observableArray([new MODELS.ClassPolicyModel()]);
            self.addClassPolicy = function() {
                self.classPolicies.push(new MODELS.ClassPolicyModel());
            };
            self.removeClassPolicy = function(policy) {
                self.classPolicies.remove(policy);
            };
        };

        models.ScheduleModel = function() {
            this.days = ko.observable().extend({
                required: true
            });
            this.startTime = ko.observable().extend({
                required: true
            });
            this.endTime = ko.observable().extend({
                required: true
            });
        };

        models.InstructorModel = function() {
            this.fullName = ko.observable().extend({
                required: true
            });
        };

        models.ElgaModel = function(number) {
            var self = this;
            self.elgaName = ko.observable().extend({
                required: true
            });

            self.learningOutcomeNumber = ko.observable(number);

            self.learningOutcome = ko.observable().extend({
                required: true
            });
        };

        models.RequiredOutputModel = function() {
            this.description = ko.observable().extend({
                required: true
            });
            this.weekDue = ko.observable().extend({
                required: true
            });
            this.los = ko.observableArray();
        };

        models.OtherOutputModel = function() {
            this.requirementName = ko.observable().extend({
                required: true
            });
        };

        models.GradingSystemModel = function() {
            this.itemName = ko.observable().extend({
                required: true
            });
            this.percentage = ko.observable().extend({
                required: true
            });
        };

        models.LearningPlanModel = function() {
            var self = this;
            self.topic = ko.observable().extend({
                required: true
            });
            self.weekNumber = ko.observable().extend({
                required: true
            });

            self.los = ko.observableArray();

            self.learningActivities = ko.observableArray([new MODELS.LearningActivityModel()]);
            self.addLearningActivity = function() {
                self.learningActivities.push(new MODELS.LearningActivityModel());
            };
            self.removeLearningActivity = function(learningActivity) {
                self.learningActivities.remove(learningActivity);
            };
        };

        models.LearningActivityModel = function() {
            this.description = ko.observable().extend({
                required: true
            });
        };

        models.ReferenceModel = function() {
            this.referenceText = ko.observable().extend({
                required: true
            });
        };

        models.ClassPolicyModel = function() {
            this.policy = ko.observable().extend({
                required: true
            });
        };

        return models;
    })(); // End models

    return MODULE;
})(Zepto, ko);

$(document).ready(function() {
    SyllabusModule.init();
});
