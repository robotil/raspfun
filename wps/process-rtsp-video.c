/********************
 * This file is building and playing the gstreamer pipeline for processing the video for the project WPS
 * It is a temporary work for the sport: 
 * It should implement the following pipeline:
 * rtspsrc location=rtsp://172.23.40.130:8554/test ! rtph264depay ! avdec_h264 ! timeoverlay halignment=right valignment=bottom ! \
 * videorate ! video/x-raw,framerate=6000/1001 ! jpegenc ! multifilesink location="./frame%08d.jpg"
 * 
 * Author: Michele Hallak-Stamler
 * Date: September 2020
 * 
 * ****************************/

#include <gst/gst.h>

/* Structure to contain all our information, so we can pass it to callbacks */
typedef struct _CustomData {
  GstElement *pipeline;
  GstElement *source;
  GstElement *rtph264Convert;
  GstElement *avdecConvert;
  GstElement *timerOverlayFilter;
  GstElement *videoRateFilter;
  GstElement *jpegConvert;
  GstElement *sink;
} CustomData;

/* Handler for the pad-added signal 
static void pad_added_handler (GstElement *src, GstPad *pad, CustomData *data);*/

int main(int argc, char *argv[]) {
  CustomData data;
  GstBus *bus;
  GstMessage *msg;
  GstStateChangeReturn ret;
  gboolean terminate = FALSE;
  GstPad *video_pad; 
  GstCaps *video_pad_caps = NULL;
  GstStructure *video_pad_struct = NULL;
  const gchar *video_pad_type = NULL;

  /* Initialize GStreamer */
  gst_init (&argc, &argv);

  /* Create the elements */
  data.source = gst_element_factory_make ("rtspsrc", "source");
  data.rtph264Convert = gst_element_factory_make ("rtph264depay", "rtph264Convert");
  data.avdecConvert = gst_element_factory_make ("avdec_h264", "avdecConvert");
  data.timerOverlayFilter = gst_element_factory_make ("timeoverlay", "timerOverlayFilter");
  data.videoRateFilter = gst_element_factory_make ("videorate", "videoRateFilter");
  data.jpegConvert = gst_element_factory_make ("jpegenc", "jpegConvert");
  data.sink = gst_element_factory_make ("multifilesink", "sink");

  /* Create the empty pipeline */
  data.pipeline = gst_pipeline_new ("rtsp-jpeg-pipeline");

  if (!data.pipeline || !data.source || !data.rtph264Convert || !data.avdecConvert || !data.timerOverlayFilter || 
          !data.videoRateFilter || !data.jpegConvert || !data.sink) {
    g_printerr ("Not all elements could be created.\n");
    return -1;
  }

  /* Build the pipeline. Note that we are NOT linking the source at this
   * point. We will do it later. */
  gst_bin_add_many (GST_BIN (data.pipeline), data.source, data.rtph264Convert, data.avdecConvert, data.timerOverlayFilter, 
  data.videoRateFilter, data.jpegConvert, data.sink, NULL);
  if (!gst_element_link_many (data.jpegConvert, data.sink, NULL)) {
    g_printerr ("Elements could not be linked.\n");
    gst_object_unref (data.pipeline);
    return -1;
  }
 if (!gst_element_link_many (data.rtph264Convert, data.avdecConvert, data.timerOverlayFilter, data.videoRateFilter, NULL)) {
    g_printerr ("Elements for video could not be linked.\n");
    gst_object_unref (data.pipeline);
    return -1;
  }
  /* Set the URI to play location=rtsp://172.23.40.130:8554/test*/
  g_object_set (data.source, "location", "rtsp://172.23.40.130:8554/test", NULL);

  /* Set cap video video/x-raw,framerate=6000/1001 */
  video_pad_caps = gst_caps_new_simple("video/x-raw", "framerate", GST_TYPE_FRACTION, 6000,1001, NULL);
  video_pad = gst_element_get_static_pad (data.videoRateFilter, "src");
  g_object_set (video_pad, "caps", video_pad_caps, NULL);

  /* Set multifilesink attribute location="./frame%08d.jpg"*/
  g_object_set(data.sink, "location", "./frame%08d.jpg", NULL );

  /* Connect to the pad-added signal */
  /*g_signal_connect (data.source, "pad-added", G_CALLBACK (pad_added_handler), &data);*/

  /* Start playing */
  ret = gst_element_set_state (data.pipeline, GST_STATE_PLAYING);
  if (ret == GST_STATE_CHANGE_FAILURE) {
    g_printerr ("Unable to set the pipeline to the playing state.\n");
    gst_object_unref (data.pipeline);
    return -1;
  }

  /* Listen to the bus */
  bus = gst_element_get_bus (data.pipeline);
  do {
    msg = gst_bus_timed_pop_filtered (bus, GST_CLOCK_TIME_NONE,
        GST_MESSAGE_STATE_CHANGED | GST_MESSAGE_ERROR | GST_MESSAGE_EOS);

    /* Parse message */
    if (msg != NULL) {
      GError *err;
      gchar *debug_info;

      switch (GST_MESSAGE_TYPE (msg)) {
        case GST_MESSAGE_ERROR:
          gst_message_parse_error (msg, &err, &debug_info);
          g_printerr ("Error received from element %s: %s\n", GST_OBJECT_NAME (msg->src), err->message);
          g_printerr ("Debugging information: %s\n", debug_info ? debug_info : "none");
          g_clear_error (&err);
          g_free (debug_info);
          terminate = TRUE;
          break;
        case GST_MESSAGE_EOS:
          g_print ("End-Of-Stream reached.\n");
          terminate = TRUE;
          break;
        case GST_MESSAGE_STATE_CHANGED:
          /* We are only interested in state-changed messages from the pipeline */
          if (GST_MESSAGE_SRC (msg) == GST_OBJECT (data.pipeline)) {
            GstState old_state, new_state, pending_state;
            gst_message_parse_state_changed (msg, &old_state, &new_state, &pending_state);
            g_print ("Pipeline state changed from %s to %s:\n",
                gst_element_state_get_name (old_state), gst_element_state_get_name (new_state));
          }
          break;
        default:
          /* We should not reach here */
          g_printerr ("Unexpected message received.\n");
          break;
      }
      gst_message_unref (msg);
    }
  } while (!terminate);

  /* Free resources */
  gst_object_unref (bus);
  gst_element_set_state (data.pipeline, GST_STATE_NULL);
  gst_object_unref (data.pipeline);
  return 0;
}
