// Misc functions

func copyFile(sourceFilePath string, destFilePath string) error {
    r, err := os.Open(sourceFilePath)
    if err != nil {
        return err
    }
    defer func() {
        if err := r.Close(); err != nil {
            log.Fatalf("os.File.Close error: %s", err)
        }
    }()
    
    w, err := os.Create(destFilePath)
    if err != nil {
        return err
    }
    defer func() {
        if err := w.Close(); err != nil {
            log.Fatalf("os.File.Close error: %s", err)
        }
    }()
    
    _, err = io.Copy(w, r)
    if err != nil {
        return err
    }
    
    return nil
}

func zipExistingFile(sourceFilePath string, destFilePath string) error {
    r, err := os.Open(sourceFilePath)
    if err != nil {
        return err
    }
    defer func() {
        if err := r.Close(); err != nil {
            log.Fatalf("os.File.Close error: %s", err)
        }
    }()
    
    zipFile, err := os.Create(destFilePath)
    if err != nil {
        return err
    }
    defer func() {
        if err := zipFile.Close(); err != nil {
            log.Fatalf("os.File.Close error: %s", err)
        }
    }()
    
    z := zip.NewWriter(zipFile)
    defer func() {
        if err := z.Close(); err != nil {
            log.Fatalf("zip.Writer.Close error: %s", err)
        }
    }()
    
    w, err := z.Create(sourceFilePath)
    if err != nil {
        return err
    }
    
    _, err = io.Copy(w, r)
    if err != nil {
        return err
    }
    
    return nil
}

func zipFolder(sourceFolderPath string, destFilePath string) error {
    zipFile, err := os.Create(destFilePath)
    if err != nil {
        return err
    }
    defer func() {
        if err := zipFile.Close(); err != nil {
            log.Fatalf("os.File.Close error: %s", err)
        }
    }()
    
    z := zip.NewWriter(zipFile)
    defer func() {
        if err := z.Close(); err != nil {
            log.Fatalf("zip.Writer.Close error: %s", err)
        }
    }()
    
    var addFileToZip = func(path string, info os.FileInfo, err error) error {
        if err != nil {
            return err
        }
        
        // Get the path of the file relative to the folder we're zipping
        relativePath, err := filepath.Rel(sourceFolderPath, path)
        if err != nil {
            return err
        }
        
        // Only include regular files, not directories
        if !info.Mode().IsRegular() {
            return nil
        }
        
        r, err := os.Open(path)
        if err != nil {
            return err
        }
        defer func() {
            if err := r.Close(); err != nil {
                log.Fatalf("os.File.Close error: %s", err)
            }
        }()
        
        w, err := z.Create(relativePath)
        if err != nil {
            return err
        }
        
        _, err = io.Copy(w, r)
        if err != nil {
            return err
        }
        
        return nil
    }
    
    err = filepath.Walk(sourceFolderPath, addFileToZip)
    if err != nil {
        return err
    }
    
    return nil
}
