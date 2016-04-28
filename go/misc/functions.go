// Misc functions

package functions

import (
	"archive/zip"
	"fmt"
	"io"
	"os"
	"path/filepath"
)

func CopyFile(sourceFilePath string, destFilePath string) error {
	r, err := os.Open(sourceFilePath)
	if err != nil {
		return err
	}
	defer func() {
		err = r.Close()
	}()

	w, err := os.Create(destFilePath)
	if err != nil {
		return err
	}
	defer func() {
		err = w.Close()
	}()

	_, err = io.Copy(w, r)
	if err != nil {
		return err
	}

	return err
}

func UnzipFile(sourceFilePath string, destDirPath string) error {
	// First, make sure the destination exists and is a directory
	info, err := os.Stat(destDirPath)
	if err != nil {
		return err
	}
	if !info.Mode().IsDir() {
		return fmt.Errorf("Destination is not a directory: %s", destDirPath)
	}

	r, err := zip.OpenReader(sourceFilePath)
	defer func() {
		if err := r.Close(); err != nil {
			panic(err)
		}
	}()

	// Iterate through each file in the archive
	for _, f := range r.File {
		rc, err := f.Open()
		if err != nil {
			return err
		}
		defer func() {
			if err := rc.Close(); err != nil {
				panic(err)
			}
		}()

		destFilePath := filepath.Join(destDirPath, f.Name)

		// Create destination subdirectories if necessary
		destBaseDirPath, _ := filepath.Split(destFilePath)
		os.MkdirAll(destBaseDirPath, testDirPerm)

		// Create the destination file
		w, err := os.Create(destFilePath)
		if err != nil {
			return err
		}
		defer func() {
			if err := w.Close(); err != nil {
				panic(err)
			}
		}()

		// Copy the contents of the source file
		_, err = io.Copy(w, rc)
		if err != nil {
			return err
		}
	}

	return nil
}

func ZipFile(sourceFilePath string, destFilePath string) error {
	r, err := os.Open(sourceFilePath)
	if err != nil {
		return err
	}
	defer func() {
		err = r.Close()
	}()

	f, err := os.Create(destFilePath)
	if err != nil {
		return err
	}
	defer func() {
		err = f.Close()
	}()

	z := zip.NewWriter(f)
	defer func() {
		err = z.Close()
	}()

	w, err := z.Create(sourceFilePath)
	if err != nil {
		return err
	}

	_, err = io.Copy(w, r)
	if err != nil {
		return err
	}

	return err
}

func ZipFolder(sourceFolderPath string, destFilePath string) error {
	f, err := os.Create(destFilePath)
	if err != nil {
		return err
	}
	defer func() {
		err = f.Close()
	}()

	z := zip.NewWriter(f)
	defer func() {
		err = z.Close()
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
			err = r.Close()
		}()

		w, err := z.Create(relativePath)
		if err != nil {
			return err
		}

		_, err = io.Copy(w, r)
		if err != nil {
			return err
		}

		return err
	}

	err = filepath.Walk(sourceFolderPath, addFileToZip)
	if err != nil {
		return err
	}

	return err
}
