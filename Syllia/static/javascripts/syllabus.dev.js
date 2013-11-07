var SyllabusModule = (function($, ko, jsonData) {
    var MODULE = {};

    MODULE.init = function() {
        var viewModel = new MODELS.SyllabusModel(jsonData);

        // ko.applyBindingsWithValidation(viewModel);
        ko.applyBindings(viewModel);
        MODULE.bindUIActions(viewModel);

        if (jsonData.syllabusData) {
            MODULE.loadData(viewModel, jsonData.syllabusData);
            viewModel.timeSinceModified(jsonData.timeSinceModified);
        }
        $(document).foundation('abide', 'events');

        Foundation.libs.forms.refresh_custom_select($('#collegeSelect'), true);
        Foundation.libs.forms.refresh_custom_select($('#departmentSelect'), true);
        Foundation.libs.forms.refresh_custom_select($('#rubricSelect'), true);

        // Foundation.libs.section.settings.callback = function(element) {
        //     console.log("Changing sections");
        //     MODULE.submitForm(viewModel, false, true);
        // };

        // Start modified timer
        if (viewModel.timeSinceModified()) {

            // If hour and day is not in the string
            if (viewModel.timeSinceModified().indexOf("hour") == -1 && viewModel.timeSinceModified().indexOf("day") == -1) {
                var modifiedTime = setInterval(function() {
                    var timeRegex = /(\d+)/g;
                    var match = timeRegex.exec(viewModel.timeSinceModified());
                    viewModel.timeSinceModified(viewModel.timeSinceModified().replace(timeRegex, parseInt(match[1]) + 1));
                }, 60000);
            }
        }
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

    MODULE.submitForm = function(viewModel, redirect, base) {
        redirect = typeof redirect !== 'undefined' ? redirect : false;
        base = typeof base !== 'undefined' ? base : false;

        if (MODULE.isValid(base)) {
            // Serialize
            var syllabus_json = ko.toJSON(viewModel, function(key, value) {
                // Ignores these fields
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

            $.ajax({
                data: {
                    'syllabus_json': syllabus_json,
                    'redirect': redirect
                },
                type: 'POST',
                url: '/syllabus/new/',
                success: function(response) {
                    if (response.redirectTo) {
                        window.location.href = response.redirectTo;
                    }

                    MODULE.loadData(viewModel, response.viewModel);
                    viewModel.timeSinceModified(response.timeSinceModified);
                }
            });
        } else {
            $('#saveBtn').toggle();
            $('#errorBtn').toggle();
            if (base)
                $('ul.messages').append($('<li></li>').attr('class', 'error').text('You must at least have basic details before saving.'));
            else
                $('ul.messages').append($('<li></li>').attr('class', 'error').text('Please check your forms.'));

            setTimeout(function() {
                $('#errorBtn').toggle();
                $('ul.messages').empty();
                $('#saveBtn').toggle();
            }, 5000);
        }
    };

    MODULE.bindUIActions = function(viewModel) {
        $('#postBtn').click(function() {
            MODULE.submitForm(viewModel, true, false);
        });

        $('#saveBtn').click(function() {
            MODULE.submitForm(viewModel, false, true);
        });

        $('#validateBtn').click(function() {
            MODULE.isValid();
        });
    };

    MODULE.isValid = function(base) {
        base = typeof base !== 'undefined' ? base : false;

        console.log('Validating...');
        var inputs = [];
        if (base) {
            $('form#baseForm[data-abide]').trigger('validate');
            inputs = $('form#baseForm[data-abide]').find('input[data-invalid], select[data-invalid], textarea[data-invalid]');
            console.log('Invalid inputs:');
            console.log(inputs.length);
        } else {
            $('form[data-abide]').trigger('validate');
            inputs = $('input[data-invalid]')
            console.log('Invalid inputs:');
        }

        return inputs.length == 0 ? true : false;
    };

    var MODELS = (function() {
        var models = {};
        models.SyllabusModel = function(jsonData) {
            var self = this;
            self.pk = null;
            self.syllabusName = ko.observable();
            self.syllabusName.subscribe(function() {
                document.title = self.syllabusName() + " | Syllia";
            });
            self.courseCode = ko.observable();
            self.courseName = ko.observable();
            self.courseDescription = ko.observable();
            self.timeSinceModified = ko.observable();

            // Dropdown lists
            self.college = ko.observable();
            self.collegeList = ko.observableArray(jsonData.collegeList);

            self.department = ko.observable();
            self.departmentList = ko.computed(function() {
                var tempList = [];

                $.each(jsonData.departmentList, function(index, value) {
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
            self.rubricList = ko.observableArray(jsonData.rubricList);

            self.schedules = ko.observableArray();
            self.addSchedule = function() {
                self.schedules.push(new MODELS.ScheduleModel());
                $(document).foundation('abide', 'events');
            };
            self.removeSchedule = function(schedule) {
                self.schedules.remove(schedule);
            };
            self.addSchedule();

            self.instructors = ko.observableArray();
            self.addInstructor = function() {
                self.instructors.push(new MODELS.InstructorModel());
                $(document).foundation('abide', 'events');
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
                $(document).foundation('abide', 'events');
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

            self.finalCourseOutputDescription = ko.observable();

            self.requiredOutputs = ko.observableArray();
            self.addRequiredOutput = function() {
                self.requiredOutputs.push(new MODELS.RequiredOutputModel());
                $(document).foundation('abide', 'events');
            };
            self.removeRequiredOutput = function(requiredOutput) {
                self.requiredOutputs.remove(requiredOutput);
            };
            self.addRequiredOutput();


            self.otherOutputs = ko.observableArray();
            self.addOtherOutput = function() {
                self.otherOutputs.push(new MODELS.OtherOutputModel());
                $(document).foundation('abide', 'events');
            };
            self.removeOtherOutput = function(otherOutput) {
                self.otherOutputs.remove(otherOutput);
            };
            self.addOtherOutput();

            // TODO: Rename this variable
            self.gradingSystems = ko.observableArray();
            self.addGradingSystem = function() {
                self.gradingSystems.push(new MODELS.GradingSystemModel());
                $(document).foundation('abide', 'events');
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
                $(document).foundation('abide', 'events');
            };
            self.removeLearningPlan = function(learningPlan) {
                self.learningPlans.remove(learningPlan);
            };
            self.addLearningPlan();

            self.references = ko.observableArray();
            self.addReference = function() {
                self.references.push(new MODELS.ReferenceModel());
                $(document).foundation('abide', 'events');
            };
            self.removeReference = function(reference) {
                self.references.remove(reference);
            };
            self.addReference();

            self.classPolicies = ko.observableArray();
            self.addClassPolicy = function() {
                self.classPolicies.push(new MODELS.ClassPolicyModel());
                $(document).foundation('abide', 'events');
            };
            self.removeClassPolicy = function(policy) {
                self.classPolicies.remove(policy);
            };
            self.addClassPolicy();
        };

        models.ScheduleModel = function(schedule) {
            var self = this;
            self.days = ko.observable();
            self.startTime = ko.observable();
            self.endTime = ko.observable();
            self.venue = ko.observable();

            if (schedule) {
                self.days(schedule.days);
                self.startTime(schedule.startTime);
                self.endTime(schedule.endTime);
                self.venue(schedule.venue);
            }
        };

        models.InstructorModel = function(instructor) {
            var self = this;
            self.fullName = ko.observable();

            if (instructor) {
                self.fullName(instructor.fullName);
            }
        };

        models.ElgaModel = function(elga) {
            var self = this;
            self.elgaName = ko.observable();
            self.learningOutcomeNumber = ko.observable();
            self.learningOutcome = ko.observable();

            // Constructor
            if (elga.learningOutcomeNumber) {
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
            self.description = ko.observable();
            self.weekDue = ko.observable();
            self.los = ko.observableArray();

            if (requiredOutput) {
                self.description(requiredOutput.description);
                self.weekDue(requiredOutput.weekDue);
                self.los(requiredOutput.los);
            }
        };

        models.OtherOutputModel = function(otherOutput) {
            var self = this;
            self.requirementName = ko.observable();

            if (otherOutput) {
                self.requirementName(otherOutput.requirementName);
            }
        };

        models.GradingSystemModel = function(gradeComponent) {
            var self = this;
            self.itemName = ko.observable();
            self.percentage = ko.observable();

            if (gradeComponent) {
                self.itemName(gradeComponent.itemName);
                self.percentage(gradeComponent.percentage);
            }
        };

        models.LearningPlanModel = function(learningPlan) {
            var self = this;
            self.topic = ko.observable();
            self.weekNumber = ko.observable();

            self.los = ko.observableArray();

            self.learningActivities = ko.observableArray();
            self.addLearningActivity = function() {
                self.learningActivities.push(new MODELS.LearningActivityModel());
                $(document).foundation('abide', 'events');
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
            self.description = ko.observable();

            if (learningActivity) {
                self.description(learningActivity.description);
            }
        };

        models.ReferenceModel = function(reference) {
            var self = this;
            self.referenceText = ko.observable();

            if (reference) {
                self.referenceText(reference.referenceText);
            }
        };

        models.ClassPolicyModel = function(classPolicy) {
            var self = this;
            self.policy = ko.observable();

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