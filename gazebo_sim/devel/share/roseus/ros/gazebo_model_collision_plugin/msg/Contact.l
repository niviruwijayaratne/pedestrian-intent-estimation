;; Auto-generated. Do not edit!


(when (boundp 'gazebo_model_collision_plugin::Contact)
  (if (not (find-package "GAZEBO_MODEL_COLLISION_PLUGIN"))
    (make-package "GAZEBO_MODEL_COLLISION_PLUGIN"))
  (shadow 'Contact (find-package "GAZEBO_MODEL_COLLISION_PLUGIN")))
(unless (find-package "GAZEBO_MODEL_COLLISION_PLUGIN::CONTACT")
  (make-package "GAZEBO_MODEL_COLLISION_PLUGIN::CONTACT"))

(in-package "ROS")
;;//! \htmlinclude Contact.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass gazebo_model_collision_plugin::Contact
  :super ros::object
  :slots (_header _objects_hit ))

(defmethod gazebo_model_collision_plugin::Contact
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:objects_hit __objects_hit) (let (r) (dotimes (i 0) (push "" r)) r))
    )
   (send-super :init)
   (setq _header __header)
   (setq _objects_hit __objects_hit)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:objects_hit
   (&optional __objects_hit)
   (if __objects_hit (setq _objects_hit __objects_hit)) _objects_hit)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; string[] _objects_hit
    (apply #'+ (mapcar #'(lambda (x) (+ 4 (length x))) _objects_hit)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; string[] _objects_hit
     (write-long (length _objects_hit) s)
     (dolist (elem _objects_hit)
       (write-long (length elem) s) (princ elem s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; string[] _objects_hit
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _objects_hit (make-list n))
     (dotimes (i n)
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setf (elt _objects_hit i) (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
     ))
   ;;
   self)
  )

(setf (get gazebo_model_collision_plugin::Contact :md5sum-) "5922a8c08ae2d9e53f76163e11e8c78c")
(setf (get gazebo_model_collision_plugin::Contact :datatype-) "gazebo_model_collision_plugin/Contact")
(setf (get gazebo_model_collision_plugin::Contact :definition-)
      "Header header
string[] objects_hit 


================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
# 0: no frame
# 1: global frame
string frame_id

")



(provide :gazebo_model_collision_plugin/Contact "5922a8c08ae2d9e53f76163e11e8c78c")


