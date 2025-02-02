document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;

            console.log(page);
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));

            // Category change
            document.querySelectorAll('input[name="categories"]').forEach(checkbox => {
                checkbox.addEventListener('change', this.filterOrganizations.bind(this));
            });
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            if (this.currentStep == 3) {
                this.filterOrganizations();
            }

            if (this.currentStep == 5) {
                this.collectFormData();
            }
        }

        /**
         * Filter organizations based on selected categories
         */
        filterOrganizations() {
            const selectedCategories = Array.from(document.querySelectorAll('input[name="categories"]:checked')).map(cb => parseInt(cb.value));
            document.querySelectorAll('input[name="organization"]').forEach(input => {
                const organizationCategories = JSON.parse(input.dataset.categories);
                const organizationElement = input.closest('.form-group');
                const isVisible = organizationCategories.some(catId => selectedCategories.includes(catId));
                organizationElement.style.display = isVisible ? '' : 'none';
            });
        }

        /**
         * Collect data from form and show in summary
         */
        collectFormData() {
            const summary = {
                categories: Array.from(document.querySelectorAll('input[name="categories"]:checked')).map(cb => cb.parentElement.querySelector('.description').innerText),
                bags: document.querySelector('input[name="bags"]').value,
                organization: document.querySelector('input[name="organization"]:checked').closest('label').querySelector('.title').innerText,
                address: {
                    street: document.querySelector('input[name="address"]').value,
                    city: document.querySelector('input[name="city"]').value,
                    postcode: document.querySelector('input[name="postcode"]').value,
                    phone: document.querySelector('input[name="phone"]').value
                },
                date: document.querySelector('input[name="data"]').value,
                time: document.querySelector('input[name="time"]').value,
                more_info: document.querySelector('textarea[name="more_info"]').value
            };

            this.displaySummary(summary);
        }

        /**
         * Display summary data in the last step
         */
        displaySummary(summary) {
            const summaryElement = document.querySelector('.summary');
            const summaryText = `
        <div class="form-section">
          <h4>Oddajesz:</h4>
          <ul>
            <li>
              <span class="icon icon-bag"></span>
              <span class="summary--text">${summary.bags} worki ${summary.categories.join(', ')}</span>
            </li>
            <li>
              <span class="icon icon-hand"></span>
              <span class="summary--text">Dla fundacji "${summary.organization}"</span>
            </li>
          </ul>
        </div>
        <div class="form-section form-section--columns">
          <div class="form-section--column">
            <h4>Adres odbioru:</h4>
            <ul>
              <li>${summary.address.street}</li>
              <li>${summary.address.city}</li>
              <li>${summary.address.postcode}</li>
              <li>${summary.address.phone}</li>
            </ul>
          </div>
          <div class="form-section--column">
            <h4>Termin odbioru:</h4>
            <ul>
              <li>${summary.date}</li>
              <li>${summary.time}</li>
              <li>${summary.more_info}</li>
            </ul>
          </div>
        </div>
      `;
            summaryElement.innerHTML = summaryText;
        }

        /**
         * Submit form
         */
        submit(e) {
            e.preventDefault();
            this.currentStep++;
            this.updateForm();

            // Sprawdź czy to jest ostatni krok formularza
            if (this.currentStep > this.slides.length) {
                this.submitForm();
            }
        }

        submitForm() {
            const formData = new FormData(this.$form.querySelector("form"));
            fetch(this.$form.querySelector("form").action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
                }
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.text();
                })
                .then(data => {
                    window.location.href = '/confirm/';
                })
                .catch(error => {
                    console.error('There has been a problem with your fetch operation:', error);
                });
        }

    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }
});
