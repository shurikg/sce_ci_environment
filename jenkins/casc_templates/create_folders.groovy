
groovy:
  - script: >
      import com.cloudbees.hudson.plugins.folder.Folder;
      import jenkins.model.Jenkins;

      def folderNames = TEMPLATE;

      folderNames.each { currentFolderName ->
        if (Jenkins.instance.getItem(currentFolderName) == null) {
          println("Create folder [" + currentFolderName + "]");
          Jenkins.instance.createProject(Folder.class, currentFolderName);
        };
      };