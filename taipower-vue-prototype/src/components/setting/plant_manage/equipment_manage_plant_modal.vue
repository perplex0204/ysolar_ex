<template>
    <div class="modal" tabindex="-1" ref="plant_create_modal">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title"> plant create </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <el-input v-model="max_usage" type="text" placeholder="test" />
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-success" @click="set_clicked"> 確定 </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { Modal } from "bootstrap";
export default {
    name: "plantModal",
    components: {
    },
    props: {
        'modalStatus': {
            type: Boolean,
        }
    },
    data() {
        return {
            screenWidth: document.body.clientWidth,
            max_usage: '',
            plant_modal_status: this.modalStatus
        }
    },

    mounted() {
        this.plant_create_modal = new Modal(
            this.$refs.plant_create_modal
        );
        let that = this;
        window.addEventListener("resize", this.plot_resize);
        window.addEventListener("resize", function () {
            return (() => {
                that.screenWidth = this.document.body.clientWidth;
            })();
        });
        if (this.screenWidth >= 576) {
            this.csvsize = "large";
            console.log("resize large");
        } else {
            this.csvsize = "small";
            console.log("resize small");
        }
    },
    unmounted() {
        window.removeEventListener("resize", this.plot_resize);
    },
    methods: {
        set_clicked() {
            this.plant_create_modal.hide();
        }
    },
    watch: {
        modalStatus: function () {
            if (this.modalStatus == true) {
                this.plant_create_modal.show();
            }
            this.plant_modal_status = false
            this.$emit('update', this.plant_modal_status)
        }
    }
}
</script>