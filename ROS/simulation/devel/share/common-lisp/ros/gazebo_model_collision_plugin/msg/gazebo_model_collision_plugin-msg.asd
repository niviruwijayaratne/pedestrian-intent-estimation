
(cl:in-package :asdf)

(defsystem "gazebo_model_collision_plugin-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "Contact" :depends-on ("_package_Contact"))
    (:file "_package_Contact" :depends-on ("_package"))
  ))