var SyllabusModule = (function($, ko, jsonData) {
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

        viewModel.schedules.removeAll();
        $.each(json.schedules, function(index, schedule) {
            viewModel.schedules.push(new MODELS.ScheduleModel(schedule));
        });

        viewModel.instructors.removeAll();
        $.each(json.instructors, function(index, instructor) {
            viewModel.instructors.push(new MODELS.InstructorModel(instructor));
        });

        viewModel.rubric(json.rubric);

        viewModel.elgas.removeAll();
        $.each(json.elgas, function(index, elga) {
            viewModel.elgas.push(new MODELS.ElgaModel(elga));
        });

        viewModel.finalCourseOutputDescription(json.finalCourseOutputDescription);

        viewModel.requiredOutputs.removeAll();
        $.each(json.requiredOutputs, function(index, requiredOutput) {
            viewModel.requiredOutputs.push(new MODELS.RequiredOutputModel(requiredOutput));
        });

        viewModel.otherOutputs.removeAll();
        $.each(json.otherOutputs, function(index, otherOutput) {
            viewModel.otherOutputs.push(new MODELS.OtherOutputModel(otherOutput));
        });

        viewModel.gradingSystems.removeAll();
        $.each(json.gradingSystems, function(index, gradeComponent) {
            viewModel.gradingSystems.push(new MODELS.GradingSystemModel(gradeComponent));
        });

        viewModel.learningPlans.removeAll();
        $.each(json.learningPlans, function(index, learningPlan) {
            viewModel.learningPlans.push(new MODELS.LearningPlanModel(learningPlan));
        });


        viewModel.references.removeAll();
        $.each(json.references, function(index, reference) {
            viewModel.references.push(new MODELS.ReferenceModel(reference));
        });

        viewModel.classPolicies.removeAll();
        $.each(json.classPolicies, function(index, classPolicy) {
            viewModel.classPolicies.push(new MODELS.ClassPolicyModel(classPolicy));
        });
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

            self.schedules = ko.observableArray();
            self.addSchedule = function() {
                self.schedules.push(new MODELS.ScheduleModel());
            };
            self.removeSchedule = function(schedule) {
                self.schedules.remove(schedule);
            };
            self.addSchedule();

            self.instructors = ko.observableArray();
            self.addInstructor = function() {
                self.instructors.push(new MODELS.InstructorModel());
            };
            self.removeInstructor = function(instructor) {
                self.instructors.remove(instructor);
            };
            self.addInstructor();

            self.elgas = ko.observableArray();
            self.addElga = function() {
                var elga = new MODELS.ElgaModel({
                    number: self.elgas().length + 1
                });
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

            self.requiredOutputs = ko.observableArray();
            self.addRequiredOutput = function() {
                self.requiredOutputs.push(new MODELS.RequiredOutputModel());
            };
            self.removeRequiredOutput = function(requiredOutput) {
                self.requiredOutputs.remove(requiredOutput);
            };
            self.addRequiredOutput();


            self.otherOutputs = ko.observableArray();
            self.addOtherOutput = function() {
                self.otherOutputs.push(new MODELS.OtherOutputModel());
            };
            self.removeOtherOutput = function(otherOutput) {
                self.otherOutputs.remove(otherOutput);
            };
            self.addOtherOutput();

            // TODO: Rename this variable
            self.gradingSystems = ko.observableArray();
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
                    var temp = parseInt(item.percentage());
                    if (!isNaN(temp))
                        total += temp;
                });

                return total;
            });
            self.addGradingSystem();

            self.learningPlans = ko.observableArray();
            self.addLearningPlan = function() {
                self.learningPlans.push(new MODELS.LearningPlanModel());
            };
            self.removeLearningPlan = function(learningPlan) {
                self.learningPlans.remove(learningPlan);
            };
            self.addLearningPlan();

            self.references = ko.observableArray();
            self.addReference = function() {
                self.references.push(new MODELS.ReferenceModel());
            };
            self.removeReference = function(reference) {
                self.references.remove(reference);
            };
            self.addReference();

            self.classPolicies = ko.observableArray();
            self.addClassPolicy = function() {
                self.classPolicies.push(new MODELS.ClassPolicyModel());
            };
            self.removeClassPolicy = function(policy) {
                self.classPolicies.remove(policy);
            };
            self.addClassPolicy();
        };

        models.ScheduleModel = function(schedule) {
            var self = this;
            self.days = ko.observable().extend({
                required: true
            });
            self.startTime = ko.observable().extend({
                required: true
            });
            self.endTime = ko.observable().extend({
                required: true
            });

            if (schedule) {
                self.days(schedule.days);
                self.startTime(schedule.startTime);
                self.endTime(schedule.endTime);
            }
        };

        models.InstructorModel = function(instructor) {
            var self = this;
            self.fullName = ko.observable().extend({
                required: true
            });

            if (instructor) {
                self.fullName(instructor.fullName);
            }
        };

        models.ElgaModel = function(elga) {
            var self = this;
            self.elgaName = ko.observable().extend({
                required: true
            });
            self.learningOutcomeNumber = ko.observable();
            self.learningOutcome = ko.observable().extend({
                required: true
            });

            // Constructor
            if (elga.elgaName) {
                self.elgaName(elga.elgaName);
                self.learningOutcomeNumber(elga.learningOutcomeNumber);
                self.learningOutcome(elga.learningOutcome);
            }

            // If empty elga
            if (elga.number) {
                self.learningOutcomeNumber(elga.number);
            }
        };

        models.RequiredOutputModel = function(requiredOutput) {
            var self = this;
            self.description = ko.observable().extend({
                required: true
            });
            self.weekDue = ko.observable().extend({
                required: true
            });
            self.los = ko.observableArray();

            if (requiredOutput) {
                self.description(requiredOutput.description);
                self.weekDue(requiredOutput.weekDue);
                self.los(requiredOutput.los);
            }
        };

        models.OtherOutputModel = function(otherOutput) {
            var self = this;
            self.requirementName = ko.observable().extend({
                required: true
            });

            if (otherOutput) {
                self.requirementName(otherOutput.requirementName);
            }
        };

        models.GradingSystemModel = function(gradeComponent) {
            var self = this;
            self.itemName = ko.observable().extend({
                required: true
            });
            self.percentage = ko.observable().extend({
                required: true
            });

            if (gradeComponent) {
                self.itemName(gradeComponent.itemName);
                self.percentage(gradeComponent.percentage);
            }
        };

        models.LearningPlanModel = function(learningPlan) {
            var self = this;
            self.topic = ko.observable().extend({
                required: true
            });
            self.weekNumber = ko.observable().extend({
                required: true
            });

            self.los = ko.observableArray();

            self.learningActivities = ko.observableArray();
            self.addLearningActivity = function() {
                self.learningActivities.push(new MODELS.LearningActivityModel());
            };
            self.removeLearningActivity = function(learningActivity) {
                self.learningActivities.remove(learningActivity);
            };
            self.addLearningActivity();

            if (learningPlan) {
                self.topic(learningPlan.topic);
                self.weekNumber(learningPlan.weekNumber);
                self.los(learningPlan.los);

                self.learningActivities.removeAll();
                $.each(learningPlan.learningActivities, function(index, learningActivity) {
                    self.learningActivities.push(new MODELS.LearningActivityModel(learningActivity));
                });
            }
        };

        models.LearningActivityModel = function(learningActivity) {
            var self = this;
            self.description = ko.observable().extend({
                required: true
            });

            if (learningActivity) {
                self.description(learningActivity.description);
            }
        };

        models.ReferenceModel = function(reference) {
            var self = this;
            self.referenceText = ko.observable().extend({
                required: true
            });

            if (reference) {
                self.referenceText(reference.referenceText);
            }
        };

        models.ClassPolicyModel = function(classPolicy) {
            var self = this;
            self.policy = ko.observable().extend({
                required: true
            });

            if (classPolicy) {
                self.policy(classPolicy.policy);
            }
        };

        return models;
    })(); // End models

    return MODULE;
})(Zepto, ko, jsonData);

$(document).ready(function() {
    SyllabusModule.init();
});
