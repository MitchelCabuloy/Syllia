(function() {
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
                    // Uncomment for test data
                    jsonData = $.parseJSON('{"courseDescription": "LBYFORE is a course that ahds-on laboratory component of FORENSC.", "classPolicies": [{"policy": "No eating", "pk": 1}, {"policy": "No cheating", "pk": 2}], "references": [{"pk": 1, "referenceText": "Reference, First"}, {"pk": 2, "referenceText": "Reference, Second"}, {"pk": 3, "referenceText": "Reference, Third"}, {"pk": 4, "referenceText": "Test reference. Saved from shell."}], "courseName": "LBYFORE", "otherOutputs": [{"pk": 1, "requirementName": "Laboratory Exam"}, {"pk": 2, "requirementName": "Group Project"}], "instructors": [{"pk": 1, "firstName": "", "lastName": "Gregory"}, {"pk": 2, "firstName": "", "lastName": "Alexi"}], "requiredOutputs": [{"los": ["LO 1: Be able to discuss different digital blah."], "pk": 1, "description": "Forensic Platform Preparation Report", "weekDue": "4"}, {"los": ["LO 2: Be able to gather artifact from different blah", "LO 3: Be able to gather artifact from different operating systems"], "pk": 2, "description": "Windows System and Artifacts Report", "weekDue": "5"}], "finalCourseOutputDescription": "Final course output description here", "college": "College of Computer Studies", "courseCode": "LBYFORE", "schedules": [{"pk": 1, "endTime": "1740", "days": "S", "startTime": "1440"}, {"pk": 2, "endTime": "1600", "days": "TH", "startTime": "1300"}], "department": "Computer Technology", "pk": 1, "elgas": [{"pk": 1, "learningOutcomes": [{"pk": 1, "description": "LO 1: Be able to discuss different digital blah."}], "elgaName": "Effective Communicator"}, {"pk": 2, "learningOutcomes": [{"pk": 2, "description": "LO 2: Be able to gather artifact from different blah"}, {"pk": 3, "description": "LO 3: Be able to gather artifact from different operating systems"}], "elgaName": "Critical/creative thinker"}], "gradingSystems": [{"pk": 1, "percentage": "60", "itemName": "Laboratory Report Average"}, {"pk": 2, "percentage": "20", "itemName": "Group Project"}, {"pk": 3, "percentage": "20", "itemName": "Laboratory Exam"}], "learningPlans": [{"topic": "Introduction / Orientation", "pk": 1, "los": [], "weekNumber": "1", "learningActivities": [{"pk": 1, "description": "Course introduction"}, {"pk": 2, "description": "Classroom policies discussion"}]}, {"topic": "1.0 Forensic Platform Preparation", "pk": 2, "los": ["LO 1: Be able to discuss different digital blah."], "weekNumber": "3", "learningActivities": [{"pk": 3, "description": "Hands-on"}]}, {"topic": "2.0 Windows Systems and Artifacts", "pk": 3, "los": ["LO 2: Be able to gather artifact from different blah", "LO 3: Be able to gather artifact from different operating systems"], "weekNumber": "4", "learningActivities": [{"pk": 4, "description": "Hands-on"}]}]}');
                    this.loadData(jsonData);
                }
            },

            defineModels: function() {
                SyllabusModel = function() {
                    var self = this;
                    self.college = ko.observable();
                    self.department = ko.observable();
                    self.courseCode = ko.observable();
                    self.courseName = ko.observable();
                    self.courseDescription = ko.observable();


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
                viewModel.pk = parseInt(json.pk)
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

                    elga.pk = parseInt(data.pk)
                    elga.elgaName(data.elgaName);

                    elga.learningOutcomes.removeAll();
                    $.each(data.learningOutcomes, function(index, lo) {
                        elga.learningOutcomes.push({
                            pk: parseInt(lo.pk),
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

                    lp.pk = parseInt(data.pk)
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

})();
