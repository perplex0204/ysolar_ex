<template>
    <div class="modal" tabindex="-1" ref="sensor_create_modal">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title"> sensor create </h5>
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
    name: "sensorModal",
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
            sensor_modal_status: this.modalStatus
        }
    },

    mounted() {
        this.sensor_create_modal = new Modal(
            this.$refs.sensor_create_modal
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
            this.sensor_create_modal.hide();
        }
    },
    watch: {
        modalStatus: function () {
            if (this.modalStatus == true) {
                this.sensor_create_modal.show();
            }
            this.sensor_modal_status = false
            this.$emit('update', this.sensor_modal_status)
        }
    }
}
</script>